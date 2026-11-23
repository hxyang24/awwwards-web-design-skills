#!/usr/bin/env python3
"""Verify standalone skill integrity and optionally seal the public source tree."""
import argparse,hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def files():return [p for p in sorted(R.rglob('*')) if p.is_file() and not any(x in p.parts for x in ['.git','node_modules','__pycache__']) and p.suffix!='.pyc' and p.name!='SOURCE_MANIFEST.json']
def digest(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def seal():
 result={'version':'page-skills-work-in-progress','scope':'Public repository source; no claim of complete site coverage','self_excluded':'SOURCE_MANIFEST.json','files':[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in files()]}
 (R/'SOURCE_MANIFEST.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def verify(check_seal=True):
 errors=[];registry=json.loads((R/'page_skills/registry.json').read_text(encoding='utf-8'));names=set()
 for s in registry['skills']:
  folder=R/s['path'];contract=json.loads((folder/'references/page-contract.json').read_text(encoding='utf-8'))
  if s['skill'] in names:errors.append('Duplicate '+s['skill'])
  names.add(s['skill'])
  if not re.search(r'^name: '+re.escape(s['skill'])+r'$',(folder/'SKILL.md').read_text(encoding='utf-8'),re.M):errors.append('Skill metadata '+s['skill'])
  if (folder/'assets/contract.json').read_bytes()!=(folder/'references/page-contract.json').read_bytes():errors.append('Contract drift '+s['skill'])
  for name,source in [('main.mjs','runtime.mjs'),('style.css','runtime.css')]:
   if digest(folder/'assets'/name)!=digest(R/'page_skills'/source):errors.append('Stale runtime '+s['skill'])
  if bool(contract['sources'])!=(s['source_coverage']=='observed_examples'):errors.append('Source-coverage claim '+s['skill'])
 if registry['status']!='in_progress':errors.append('Full-site completion requires a separate goal audit')
 if check_seal:
  expected=json.loads((R/'SOURCE_MANIFEST.json').read_text(encoding='utf-8'))['files'];expected_paths={x['path'] for x in expected};actual_paths={p.relative_to(R).as_posix() for p in files()}
  for x in expected:
   p=R/x['path']
   if not p.is_file() or p.stat().st_size!=x['bytes'] or digest(p)!=x['sha256']:errors.append('Sealed file changed: '+x['path'])
  if actual_paths!=expected_paths:errors.append('Repository inventory changed')
 return {'status':'failed' if errors else 'passed','core_skills':24,'page_skills':len(names),'full_site_status':'in_progress','errors':errors}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seal',action='store_true');p.add_argument('--structure-only',action='store_true');a=p.parse_args()
 if a.seal:seal()
 result=verify(not a.structure_only);print(json.dumps(result,ensure_ascii=True,indent=2));raise SystemExit(result['status']!='passed')
