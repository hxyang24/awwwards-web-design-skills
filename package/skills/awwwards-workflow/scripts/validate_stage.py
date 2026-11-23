#!/usr/bin/env python3
"""Validate stage ledger; never turn absence of evidence into success."""
import argparse,json,sys
from pathlib import Path
VALID={'passed','failed','blocked','not_run','partial'}
def validate(project):
 logs=[]
 try: spec=json.loads((project/'PROJECT.json').read_text(encoding='utf-8'))
 except Exception as e:return [{'file':'PROJECT.json','errors':[str(e)]}]
 for stage in spec['stages']:
  fp=project/'stages'/f'{stage}.json'; errs=[]
  try: d=json.loads(fp.read_text(encoding='utf-8'))
  except Exception as e:logs.append({'stage':stage,'status':'invalid','errors':[str(e)]});continue
  state=d.get('status')
  if state not in VALID:errs.append(f'invalid status: {state}')
  if d.get('stage')!=stage:errs.append('stage mismatch')
  for item in d.get('artifacts',[]):
   rp=item.get('path') if isinstance(item,dict) else str(item)
   if not rp or not (project/rp).is_file(): errs.append(f'missing artifact: {rp}')
  for i,t in enumerate(d.get('tests',[])):
   if not isinstance(t,dict) or t.get('status') not in VALID:errs.append(f'invalid test {i}');continue
   if t['status']=='passed' and not t.get('evidence'):errs.append(f'test {i}: passed with no evidence')
   if t['status']=='passed' and t.get('evidence_type')=='file' and not (project/t['evidence']).is_file():errs.append(f'test {i}: evidence file missing')
  if state=='passed':
   if not d.get('artifacts'):errs.append('passed stage without artifacts')
   if not d.get('tests'):errs.append('passed stage without tests')
   if any(t.get('status')!='passed' for t in d.get('tests',[]) if isinstance(t,dict)):errs.append('passed stage with nonpassed test')
  logs.append({'stage':stage,'status':state,'errors':errs})
 return logs
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--project',type=Path,required=True);args=p.parse_args();r=validate(args.project)
 print(json.dumps({'ok':not any(x['errors'] for x in r),'fully_verified':bool(r) and all(x['status']=='passed' for x in r),'stages':r},ensure_ascii=False,indent=2))
 sys.exit(1 if any(x['errors'] for x in r) else 0)
