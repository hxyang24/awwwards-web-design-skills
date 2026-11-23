#!/usr/bin/env python3
import hashlib,json,re,argparse
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(check_manifest=True):
 errors=[];old=json.loads((R/'v2/contracts/v1-file-hashes.json').read_text(encoding='utf-8'))
 for row in old:
  p=R/row['path']
  if not p.is_file() or digest(p)!=row['sha256']:errors.append('V1 mismatch: '+row['path'])
 skills=list((R/'skills').glob('*/SKILL.md'))
 for p in skills:
  text=p.read_text(encoding='utf-8')
  if not text.startswith('---') or not re.search(r'^name: '+re.escape(p.parent.name)+r'$',text,re.M) or not re.search(r'^description: .+',text,re.M):errors.append('Skill metadata: '+p.parent.name)
  for link in re.findall(r'\]\(([^)]+)\)',text):
   if not re.match(r'https?://',link) and not (p.parent/link).exists():errors.append('Skill link: '+str(p)+' -> '+link)
 patterns=json.loads((R/'v2/library/page-patterns.json').read_text(encoding='utf-8'))['patterns'];ids=set()
 for p in patterns:
  if p['id'] in ids:errors.append('Duplicate pattern '+p['id'])
  ids.add(p['id'])
  if not (R/'skills'/p['skill']/'SKILL.md').is_file():errors.append('Unknown pattern skill '+p['id'])
  if p['coverage'] not in ['specification','runnable_demo'] or p['production']!='not_connected':errors.append('Coverage state '+p['id'])
  if p['coverage']=='runnable_demo' and not (R/p['demo'].split('#')[0].lstrip('/')/'index.html').is_file():errors.append('Demo missing '+p['id'])
 manifest=R/'MANIFEST-V2.json'
 if check_manifest and manifest.exists():
  for row in json.loads(manifest.read_text(encoding='utf-8'))['files']:
   p=R/row['path']
   if not p.is_file() or p.stat().st_size!=row['bytes'] or digest(p)!=row['sha256']:errors.append('Manifest mismatch: '+row['path'])
 return {'status':'failed' if errors else 'passed','v1_original_files':len(old),'skills':len(skills),'patterns':len(patterns),'runnable_routes':sum(p['coverage']=='runnable_demo' for p in patterns),'manifest_checked':check_manifest and manifest.exists(),'errors':errors}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--structure-only',action='store_true',help='Check contracts and V1 preservation, not sealed evidence hashes');args=parser.parse_args()
 result=verify(not args.structure_only);print(json.dumps(result,ensure_ascii=True,indent=2));raise SystemExit(result['status']!='passed')
