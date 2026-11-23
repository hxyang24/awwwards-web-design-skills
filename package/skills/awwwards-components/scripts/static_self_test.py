#!/usr/bin/env python3
import tempfile,subprocess,sys,json
from pathlib import Path
skill=Path(__file__).resolve().parents[1]
root=Path(__file__).resolve().parents[3]
results=[]
with tempfile.TemporaryDirectory() as tmp:
 for kind in ('saas','commerce','dashboard','portfolio','editorial','immersive'):
  dst=Path(tmp)/kind
  cmd=[sys.executable,str(skill/'scripts/scaffold.py'),'--kind',kind,'--name','自测品牌','--output',str(dst)]
  p=subprocess.run(cmd,capture_output=True,text=True)
  if p.returncode:raise AssertionError(p.stderr)
  p=subprocess.run([sys.executable,str(root/'skills/awwwards-quality/scripts/static_audit.py'),str(dst/'index.html')],capture_output=True,text=True)
  results.append({'kind':kind,'passed':p.returncode==0,'details':json.loads(p.stdout)})
print(json.dumps({'passed':all(x['passed'] for x in results),'templates':results},ensure_ascii=False,indent=2))
sys.exit(0 if all(x['passed'] for x in results) else 1)
