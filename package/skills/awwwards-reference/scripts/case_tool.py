#!/usr/bin/env python3
"""Cited desk research, not a substitute for live inspection."""
import argparse,json,sys
from pathlib import Path
DATA=Path(__file__).resolve().parents[3]/'research/cases/representative_30.json'
def validate(cs):
 errors=[];ids=set()
 for c in cs:
  id=c.get('case_id');sources={x.get('id') for x in c.get('sources',[])}
  if id in ids:errors.append(f'duplicate {id}')
  ids.add(id)
  for fact in c.get('facts',[]):
   if not fact.get('source_ids') or not set(fact['source_ids']).issubset(sources):errors.append(f'{id} unsupported fact {fact.get("id")}')
  if c.get('research_level')=='desk_researched' and c.get('inspection_plan',{}).get('status')=='passed':errors.append(f'{id} invalid live claim')
  for b in c.get('blueprints',[]):
   for key in ('inputs','states','steps','outputs','fallback','cleanup','acceptance'):
    if not b.get(key):errors.append(f'{id} blueprint missing {key}')
 return errors
if __name__=='__main__':
 p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True); sub.add_parser('list');sub.add_parser('validate');show=sub.add_parser('show');show.add_argument('--id',required=True);a=p.parse_args();d=json.loads(DATA.read_text(encoding='utf-8'));cs=d['cases']
 if a.cmd=='list':
  for c in cs:print(f"{c['case_id']:40} {c['name']:38} {c['research_level']}")
 elif a.cmd=='show':
  c=next((x for x in cs if x['case_id']==a.id),None)
  if not c:sys.exit('ID not found')
  print(json.dumps(c,ensure_ascii=False,indent=2))
 else:
  e=validate(cs);print(json.dumps({'ok':not e,'cases':len(cs),'errors':e},ensure_ascii=False,indent=2));sys.exit(bool(e))
