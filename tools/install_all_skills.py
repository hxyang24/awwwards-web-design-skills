#!/usr/bin/env python3
"""Install preserved core skills and new standalone page skills, without overwrite."""
from pathlib import Path
import argparse,json,shutil
R=Path(__file__).resolve().parents[1]
def install(target):
 dest=Path(target).expanduser().resolve()
 if dest==R or R in dest.parents:raise ValueError('Choose a target outside the source repository')
 sources=sorted([* (R/'package/skills').glob('*/SKILL.md'),* (R/'skills').glob('*/SKILL.md')]);names=[p.parent.name for p in sources]
 if len(names)!=len(set(names)):raise ValueError('Duplicate skill names in source')
 dest.mkdir(parents=True,exist_ok=True);rows=[]
 for p in sources:
  target_skill=dest/p.parent.name
  if target_skill.exists() or target_skill.is_symlink():rows.append({'skill':p.parent.name,'status':'skipped_existing'});continue
  shutil.copytree(p.parent,target_skill)
  if (p.parent/'references/contract.md').exists() and p.is_relative_to(R/'package/skills'):(target_skill/'PACKAGE_LOCATION.json').write_text(json.dumps({'package_root':str(R/'package'),'version':'2.0.1'},indent=2)+'\n',encoding='utf-8')
  rows.append({'skill':p.parent.name,'status':'installed'})
 return rows
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--target');p.add_argument('--list',action='store_true');a=p.parse_args()
 if a.list:print(json.dumps(sorted(p.parent.name for base in [R/'skills',R/'package/skills'] for p in base.glob('*/SKILL.md')),indent=2))
 elif a.target:
  try:print(json.dumps(install(a.target),indent=2))
  except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
 else:p.error('--list or --target required')
