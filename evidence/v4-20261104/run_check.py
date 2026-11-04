import subprocess,json,datetime,pathlib,hashlib,sys
root=pathlib.Path.cwd(); dest=root/"evidence/v4-20261104"
label=sys.argv[1]; args=sys.argv[2:]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
run=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
log=dest/(label+".log"); log.write_text(run.stdout)
receipt={"test_id":label,"checked_at_utc":start,"ended_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"head_sha":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),"command":args,"mode":"fixture","exit_code":run.returncode,"log":str(log.relative_to(root)),"log_sha256":hashlib.sha256(log.read_bytes()).hexdigest(),"diff_sha256":hashlib.sha256(subprocess.check_output(["git","diff","HEAD"])).hexdigest()}
(dest/(label+".json")).write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt));print("\n".join(run.stdout.splitlines()[-18:]))
sys.exit(run.returncode)
