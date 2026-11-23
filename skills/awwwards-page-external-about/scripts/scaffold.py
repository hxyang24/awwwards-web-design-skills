#!/usr/bin/env python3
from pathlib import Path
import argparse,shutil,json
source=Path(__file__).resolve().parents[1]/'assets'
def scaffold(output):
 target=Path(output).expanduser().resolve()
 if target==source or source in target.parents:raise ValueError('Choose a directory outside skill assets')
 if target.exists() and any(target.iterdir()):raise ValueError('Refusing to overwrite a nonempty directory')
 target.mkdir(parents=True,exist_ok=True)
 for p in source.iterdir():shutil.copy2(p,target/p.name)
 return {'output':str(target),'start':'python -m http.server 8000 --bind 127.0.0.1','mode':'local_original_preview'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
 try:print(json.dumps(scaffold(a.output)))
 except (OSError,ValueError) as e:p.exit(2,str(e)+'\n')
