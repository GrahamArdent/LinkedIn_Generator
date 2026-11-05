from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
manifest=json.loads((root/"FILES.sha256.json").read_text())
for name,want in manifest.items():
 got=hashlib.sha256((root/name).read_bytes()).hexdigest()
 if got!=want:raise SystemExit("HASH_MISMATCH "+name)
print("PASS",len(manifest),"saved files verified; no provider calls")
