#!/usr/bin/env python3
"""Create/verify evidence manifest; package manifest omits itself to prevent hash recursion."""
import argparse,json,hashlib,sys
from pathlib import Path

def sha256(f):
 h=hashlib.sha256()
 with f.open('rb') as fp:
  while b:=fp.read(1024*1024):h.update(b)
 return h.hexdigest()
def manifest(root,output):
 files=[]
 for f in sorted(root.rglob('*')):
  if not f.is_file() or f.resolve()==output.resolve() or '__pycache__' in f.parts or '.git' in f.parts:continue
  files.append({'path':f.relative_to(root).as_posix(),'bytes':f.stat().st_size,'sha256':sha256(f)})
 return {'schema_version':'1.0','root':'.','file_count':len(files),'files':files,'warning':'Hash integrity only. Does not prove browser testing, sources truth, licensing, or production deployment.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',required=True,type=Path);grp=p.add_mutually_exclusive_group(required=True);grp.add_argument('--output',type=Path);grp.add_argument('--verify',type=Path);a=p.parse_args();root=a.root.resolve()
 if a.output:
  out=a.output.resolve();out.parent.mkdir(parents=True,exist_ok=True);d=manifest(root,out);out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'created':str(out),'files':len(d['files'])},ensure_ascii=False))
 else:
  data=json.loads(a.verify.read_text(encoding='utf-8'));problems=[]
  for f in data['files']:
   path=(root/f['path']).resolve()
   if not path.is_relative_to(root) or not path.is_file():problems.append('missing or unsafe: '+f['path']);continue
   if f['sha256']!=sha256(path):problems.append('sha mismatch: '+f['path'])
  print(json.dumps({'passed':not problems,'checked':len(data['files']),'errors':problems},ensure_ascii=False));sys.exit(bool(problems))
