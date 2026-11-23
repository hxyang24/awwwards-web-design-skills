#!/usr/bin/env python3
"""Exit 2 for no measurement, 1 for failure, 0 for evidenced pass."""
import argparse,json,sys
from pathlib import Path
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('path',type=Path);a=p.parse_args();d=json.loads(a.path.read_text(encoding='utf-8'))
 if d.get('status')!='measured':
  print(json.dumps({'passed':False,'status':d.get('status','not_run'),'reason':'no real measurement, cannot pass'},ensure_ascii=False));sys.exit(2)
 issues=[]
 for k in ('source','measured_at','device','percentile','sample_count','lcp_ms','inp_ms','cls'):
  if d.get(k) is None:issues.append('missing '+k)
 if not issues and (d['percentile']!=75 or d['sample_count']<1):issues.append('needs 75th percentile and positive sample count')
 if not issues:
  for k,bound in [('lcp_ms',2500),('inp_ms',200),('cls',0.1)]:
   if not isinstance(d[k],(float,int)) or d[k]>bound:issues.append(f'{k} exceeds budget {bound}')
 print(json.dumps({'passed':not issues,'status':'passed' if not issues else 'failed','issues':issues},ensure_ascii=False,indent=2));sys.exit(bool(issues))
