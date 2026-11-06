"""Local canonical identity and immutable artifacts, outside all release trees."""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import time
import uuid


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()


def sha(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def atomic(path, raw):
    path=Path(path)
    temporary=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    with temporary.open('xb') as stream:
        os.chmod(temporary,0o600);stream.write(raw);stream.flush();os.fsync(stream.fileno())
    os.replace(temporary,path)
    fd=os.open(path.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)


class Store:
    def __init__(self, root):
        self.root=Path(root).resolve()
        if not self.root.exists():raise ValueError('STORE_NOT_INITIALIZED')
        try:
            marker=json.loads((self.root/'store.json').read_bytes())
            db=self.root/'registry.sqlite3'
            if not db.is_file() or not (self.root/'blobs').is_dir():raise ValueError()
            with self.connection() as con:
                if con.execute('PRAGMA quick_check').fetchone()[0]!='ok':raise ValueError()
                if con.execute('SELECT value FROM metadata WHERE key="identity"').fetchone()[0]!=marker['identity']:raise ValueError()
        except (OSError,ValueError,KeyError,TypeError,sqlite3.Error):
            raise ValueError('STORE_CORRUPT') from None

    @classmethod
    def initialize(cls, root):
        root=Path(root).resolve()
        # Explicit initialization must never reset even a partially damaged store.
        if root.exists():return cls(root)
        root.mkdir(parents=True,mode=0o700)
        (root/'blobs').mkdir(mode=0o700);(root/'jobs').mkdir(mode=0o700)
        identity=uuid.uuid4().hex
        with sqlite3.connect(root/'registry.sqlite3') as con:
            con.executescript('''
            CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
            CREATE TABLE jobs(id TEXT PRIMARY KEY,input TEXT NOT NULL,binding TEXT NOT NULL,state TEXT NOT NULL,created REAL NOT NULL,result_hash TEXT);
            CREATE TABLE stages(job TEXT NOT NULL,name TEXT NOT NULL,input_hash TEXT NOT NULL,state TEXT NOT NULL,result_hash TEXT,PRIMARY KEY(job,name));
            CREATE TABLE events(id INTEGER PRIMARY KEY,job TEXT NOT NULL,kind TEXT NOT NULL,payload_hash TEXT NOT NULL);
            ''')
            con.execute('INSERT INTO metadata VALUES (?,?)',('identity',identity))
            con.execute('INSERT INTO metadata VALUES (?,?)',('trial_history',json.dumps({'status':'unreconciled','known_topics':[],'max_subjects':8,'first_six':'Import retained original history before new trials'})))
        atomic(root/'store.json',encoded({'identity':identity,'version':1}))
        return cls(root)

    def connection(self):
        con=sqlite3.connect('file:'+str(self.root/'registry.sqlite3')+'?mode=rw',uri=True,timeout=30)
        con.row_factory=sqlite3.Row
        con.execute('PRAGMA synchronous=FULL')
        return con

    @contextmanager
    def transaction(self):
        con=self.connection()
        try:
            con.execute('BEGIN IMMEDIATE');yield con;con.commit()
        except BaseException:con.rollback();raise
        finally:con.close()

    def blob(self,value):
        raw=encoded(value);key=hashlib.sha256(raw).hexdigest();path=self.root/'blobs'/key
        if path.exists():
            if path.read_bytes()!=raw:raise ValueError('STORE_CORRUPT')
        else:atomic(path,raw)
        return key

    def read_blob(self,key):
        try:
            if len(key)!=64 or any(c not in '0123456789abcdef' for c in key):raise ValueError()
            raw=(self.root/'blobs'/key).read_bytes()
            if hashlib.sha256(raw).hexdigest()!=key:raise ValueError()
            return json.loads(raw)
        except (OSError,ValueError,TypeError):raise ValueError('STORE_CORRUPT') from None

    def admit(self,job,inputs,binding):
        if not isinstance(job,str) or not job.strip() or len(job)>100:raise ValueError('INVALID_JOB_ID')
        with self.transaction() as con:
            old=con.execute('SELECT * FROM jobs WHERE id=?',(job,)).fetchone()
            if old:
                if json.loads(old['input'])!=inputs:raise ValueError('REQUEST_CONFLICT')
            else:
                con.execute('INSERT INTO jobs VALUES (?,?,?,?,?,NULL)',(job,encoded(inputs).decode(),encoded(binding).decode(),'prepared',time.time()))
        return self.get(job)

    def get(self,job):
        with self.connection() as con:row=con.execute('SELECT * FROM jobs WHERE id=?',(job,)).fetchone()
        if row is None:raise ValueError('JOB_NOT_FOUND')
        data=dict(row);data['input']=json.loads(data['input']);data['binding']=json.loads(data['binding'])
        if data['result_hash']:data['result']=self.read_blob(data['result_hash'])
        return data

    def list(self):
        with self.connection() as con:ids=[r[0] for r in con.execute('SELECT id FROM jobs ORDER BY created')]
        return [self.get(i) for i in ids]

    def directory(self,job):
        self.get(job)
        path=self.root/'jobs'/hashlib.sha256(job.encode()).hexdigest()
        path.mkdir(mode=0o700,exist_ok=True)
        return path

    def finish(self,job,state,result):
        with self.transaction() as con:
            key=self.blob(result)
            row=con.execute('SELECT state,result_hash FROM jobs WHERE id=?',(job,)).fetchone()
            if row is None:raise ValueError('JOB_NOT_FOUND')
            if row['state']=='completed' and (row['result_hash']!=key or state!='completed'):raise ValueError('IMMUTABLE_RESULT')
            con.execute('UPDATE jobs SET state=?,result_hash=? WHERE id=?',(state,key,job))
        return self.get(job)

    def reserve(self,job,name,inputs):
        self.get(job)
        with self.transaction() as con:
            row=con.execute('SELECT * FROM stages WHERE job=? AND name=?',(job,name)).fetchone()
            if row:
                if row['input_hash']!=sha(inputs):raise ValueError('STAGE_CONFLICT')
                if row['state']=='completed':
                    self.read_blob(row['result_hash']);return 'completed'
                raise ValueError('RECONCILIATION_REQUIRED')
            con.execute('INSERT INTO stages VALUES (?,?,?,?,NULL)',(job,name,sha(inputs),'reserved'))
        return 'reserved'

    def stage(self,job,name):
        with self.connection() as con:row=con.execute('SELECT * FROM stages WHERE job=? AND name=?',(job,name)).fetchone()
        return self.read_blob(row['result_hash']) if row and row['state']=='completed' else None

    def commit_stage(self,job,name,result):
        with self.transaction() as con:
            key=self.blob(result)
            row=con.execute('SELECT * FROM stages WHERE job=? AND name=?',(job,name)).fetchone()
            if row is None:raise ValueError('STAGE_NOT_RESERVED')
            if row['state']=='completed' and row['result_hash']!=key:raise ValueError('IMMUTABLE_RESULT')
            con.execute('UPDATE stages SET state="completed",result_hash=? WHERE job=? AND name=?',(key,job,name))

    def event(self,job,kind,payload):
        self.get(job)
        with self.transaction() as con:
            key=self.blob(payload)
            con.execute('INSERT INTO events(job,kind,payload_hash) VALUES (?,?,?)',(job,kind,key))
        return payload

    def events(self,job):
        with self.connection() as con:rows=con.execute('SELECT kind,payload_hash FROM events WHERE job=? ORDER BY id',(job,)).fetchall()
        return [{'kind':r['kind'],'payload':self.read_blob(r['payload_hash'])} for r in rows]

    def backup(self,destination):
        import shutil
        destination=Path(destination)
        if destination.exists():raise ValueError('BACKUP_DESTINATION_EXISTS')
        # Serialize registry and blob writers for a consistent snapshot.
        with self.transaction():
            destination.mkdir(mode=0o700,parents=True)
            with self.connection() as source,sqlite3.connect(destination/'registry.sqlite3') as target:source.backup(target)
            shutil.copytree(self.root/'blobs',destination/'blobs')
            shutil.copytree(self.root/'jobs',destination/'jobs')
            shutil.copy2(self.root/'store.json',destination/'store.json')
        Store(destination)
