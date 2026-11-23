#!/usr/bin/env python3
"""Focused contract validator, not a general JSON Schema engine."""
import argparse,json
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def validate(kind,data,base=R):
 errors=[]
 if kind=='reference':
  for k in ['source','viewport','state','observations','hypotheses','unknowns']:
   if k not in data:errors.append('Missing '+k)
  source=data.get('source',{})
  if not source.get('permission') or not (source.get('path') or source.get('url')):errors.append('Source and permission are required')
  for k in ['width','height','device_scale_factor']:
   v=data.get('viewport',{}).get(k)
   if not isinstance(v,(int,float)) or isinstance(v,bool) or v<=0:errors.append('Invalid viewport '+k)
  for x in data.get('observations',[]):
   if not x.get('fact') or not x.get('evidence'):errors.append('Observed facts need evidence')
 elif kind=='acceptance':
  checks=data.get('checks',[])
  if not checks:errors.append('No acceptance checks')
  ids=set()
  for c in checks:
   if not c.get('id') or c['id'] in ids:errors.append('Missing or duplicate check id')
   ids.add(c.get('id'))
   if c.get('status') not in ['passed','failed','blocked','not_run']:errors.append('Invalid status')
   if c.get('status')=='passed':
    if not c.get('method') or not c.get('environment') or not c.get('evidence'):errors.append('Passed needs method, environment and evidence')
    for name in c.get('evidence',[]):
     if not isinstance(name,str):errors.append('Invalid evidence path');continue
     p=(base/name).resolve()
     if not p.is_relative_to(base.resolve()) or not p.is_file():errors.append('Missing or out-of-scope evidence: '+name)
   if c.get('status')=='blocked' and not c.get('reason'):errors.append('Blocked check needs a reason')
 else:errors.append('Unknown contract kind')
 return errors
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('kind',choices=['reference','acceptance']);p.add_argument('file');a=p.parse_args()
 try:errors=validate(a.kind,json.loads(Path(a.file).read_text(encoding='utf-8')))
 except (OSError,ValueError,TypeError) as e:errors=[str(e)]
 print(json.dumps({'status':'failed' if errors else 'passed','scope':'Contract structure and local evidence existence only','errors':errors},ensure_ascii=True));raise SystemExit(bool(errors))
