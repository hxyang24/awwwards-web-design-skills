#!/usr/bin/env python3
"""Standalone artifact and source-evidence checks for distinct mechanisms."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,platform,sys,tempfile,unittest
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'))
from build_interaction_skills import asset_digest
from build_page_skills import definitions
REG=json.loads((R/'interaction_skills/registry.json').read_text(encoding='utf-8'))

class Patterns(unittest.TestCase):
 def test_exports_are_self_contained_and_refuse_existing_project(self):
  with tempfile.TemporaryDirectory() as directory:
   for row in REG['skills']:
    source=R/row['path'];spec=importlib.util.spec_from_file_location(row['id'],source/'scripts/scaffold.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    target=Path(directory)/row['id'];module.scaffold(target)
    self.assertEqual(asset_digest(target),row['asset_sha256'])
    for f in ['index.html','main.mjs','style.css']:self.assertTrue((target/f).is_file())
    marker=target/'my-project.txt';marker.write_text('preserve')
    with self.assertRaises(ValueError):module.scaffold(target)
    self.assertEqual(marker.read_text(),'preserve')
 def test_source_claims_resolve_without_promoting_fallback_to_success(self):
  evidence={x['id']:x for x in json.loads((R/'research/live_pages/interaction-observations.json').read_text(encoding='utf-8'))['observations']}
  for row in REG['skills']:
   c=json.loads((R/row['path']/'references/pattern-contract.json').read_text(encoding='utf-8'))
   self.assertFalse(c['source_reproduction_claim']);self.assertFalse(c['source_screenshots_redistributed']);self.assertFalse(row['source_normal_experience_validated'])
   self.assertEqual(c['source_evidence'],[evidence[x] for x in row['source_observation_ids']])
   self.assertTrue(c['limits']);self.assertTrue(c['invariants'])
  self.assertIn('fallback',str(evidence['active-theory-compatibility-fallback']).lower())
 def test_three_vendor_retains_license_and_matches_preserved_library(self):
  folder=R/'skills/awwwards-pattern-immersive-fallback/assets/vendor'
  for name in ['three.module.js','three.core.js','LICENSE']:
   with (folder/name).open('rb') as f:a=hashlib.file_digest(f,'sha256').hexdigest()
   with (R/'package/v2/vendor/three'/name).open('rb') as f:b=hashlib.file_digest(f,'sha256').hexdigest()
   self.assertEqual(a,b)
  self.assertIn('MIT License',(folder/'LICENSE').read_text(encoding='utf-8'))
 def test_mechanisms_are_distinct_assets_and_have_valid_support_targets(self):
  declared={p.parent.name for root in [R/'skills',R/'package/skills'] for p in root.glob('*/SKILL.md')}
  self.assertEqual(len(declared),24+len(definitions())+REG['interaction_skills']);self.assertEqual(len({r['asset_sha256'] for r in REG['skills']}),3)
  for row in REG['skills']:
   for target in row['supports_page_skills']:self.assertIn(target,declared)
   self.assertEqual(asset_digest(R/row['path']/'assets'),row['asset_sha256'])
 def test_careers_landing_uses_source_backed_specialized_runtime(self):
  row=next(x for x in json.loads((R/'page_skills/registry.json').read_text(encoding='utf-8'))['skills'] if x['id']=='external-careers')
  self.assertEqual(row['kind'],'careers');self.assertEqual(row['runtime_variant'],'careers-pattern')
  c=json.loads((R/row['path']/'references/page-contract.json').read_text(encoding='utf-8'));self.assertGreater(len(c['sources']),0)
  self.assertNotIn('accommodation',c['sources'][0]['url']);self.assertIn('values-gallery',(R/row['path']/'assets/index.html').read_text(encoding='utf-8'))

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Patterns))
 folder=R/'research/interaction_skill_validation';folder.mkdir(parents=True,exist_ok=True)
 (folder/'unit-results.json').write_text(json.dumps({'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'passed' if result.wasSuccessful() else 'failed','tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'platform':platform.system(),'scope':'Standalone exports, evidence boundaries, license preservation and specialized careers runtime'},indent=2)+'\n',encoding='utf-8',newline='\n')
 raise SystemExit(not result.wasSuccessful())
