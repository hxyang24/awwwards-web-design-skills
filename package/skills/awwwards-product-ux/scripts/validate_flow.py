#!/usr/bin/env python3
"""Detect fake success, missing error recovery, and unsafe backend assumptions."""
import json,sys,argparse
from pathlib import Path
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('path',type=Path);a=p.parse_args();d=json.loads(a.path.read_text(encoding='utf-8'));e=[]
 mode=d.get('mode')
 if mode not in ('preview','production'):e.append('mode must preview or production')
 states=set(d.get('states',[]))
 if not {'idle','loading','success','error'}.issubset(states):e.append('basic states missing')
 if not d.get('user_goal') or not d.get('primary_action'):e.append('user goal/action missing')
 for t in d.get('transitions',[]):
  if t.get('from') not in states or t.get('to') not in states:e.append(f'invalid transition: {t}')
 if 'error' in states and not any(x.get('from')=='error' and x.get('to') in ('idle','loading') for x in d.get('transitions',[])):e.append('no error recovery path')
 if mode=='preview':
  if d.get('network_effect') not in ('none','local_simulation'):e.append('preview cannot claim real side effect')
  if not d.get('preview_disclaimer'):e.append('preview disclaimer missing')
 if mode=='production':
  api=d.get('backend_contract',{})
  if not api.get('endpoint') or not api.get('auth') or not api.get('error_codes'):e.append('production backend contract incomplete')
  if d.get('operation') in ('payment','order','upload') and not api.get('server_authoritative_status'):e.append('server authoritative status required')
 print(json.dumps({'passed':not e,'errors':e,'mode':mode},ensure_ascii=False,indent=2));sys.exit(bool(e))
