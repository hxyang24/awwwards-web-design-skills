#!/usr/bin/env python3
import sys,json,argparse
from pathlib import Path
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('path',type=Path);a=p.parse_args();d=json.loads(a.path.read_text(encoding='utf-8'));errs=[]
 for k in ('name','target','trigger','initial_state','end_state','duration_ms','reduced_motion','cleanup','fallback'):
  if k not in d or d[k] in ('',None):errs.append('missing '+k)
 if d.get('duration_ms',-1)<0 or d.get('duration_ms',99999)>5000:errs.append('duration outside 0-5000ms')
 if d.get('fallback')=='none' or d.get('reduced_motion')=='none':errs.append('no fallback or reduced motion')
 print(json.dumps({'passed':not errs,'errors':errs},ensure_ascii=False,indent=2));sys.exit(bool(errs))
