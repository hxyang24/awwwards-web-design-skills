#!/usr/bin/env python3
from pathlib import Path
import argparse,shutil,json
SOURCE=Path(__file__).resolve().parents[1]/'assets'
def scaffold(output):
 target=Path(output).expanduser().resolve()
 if target==SOURCE or SOURCE in target.parents:raise ValueError('Choose a directory outside the source assets')
 if target.exists() and any(target.iterdir()):raise ValueError('Refusing to overwrite a nonempty directory')
 target.mkdir(parents=True,exist_ok=True)
 for p in SOURCE.iterdir():
  if p.is_dir():shutil.copytree(p,target/p.name)
  else:shutil.copy2(p,target/p.name)
 return {'mode':'original_local_pattern','output':str(target),'start':'python -m http.server 8000 --bind 127.0.0.1'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
 try:print(json.dumps(scaffold(a.output)))
 except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
