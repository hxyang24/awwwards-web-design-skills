import sys,unittest,tempfile,json,subprocess,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from install import install
from validate_contract import validate,R
from scaffold import scaffold,KINDS
from route_task import route
class Tools(unittest.TestCase):
 def test_router_combines_business_and_visual_tasks_without_losing_legacy_entry(self):
  names=route('金融交易终端按照截图重建')['suggested_skills']
  for name in ['awwwards-workflow','awwwards-fintech','awwwards-design-intelligence','awwwards-visual-reconstruction','awwwards-visual-diff','awwwards-acceptance-docs']:self.assertIn(name,names)
  self.assertEqual(len(names),len(set(names)))
 def test_router_outputs_available_skills_for_unknown_task(self):
  for name in route('an unspecified design request')['suggested_skills']:self.assertTrue((R/'skills'/name/'SKILL.md').is_file())
 def test_all_new_templates_export_with_runtime_and_no_overwrite(self):
  with tempfile.TemporaryDirectory() as d:
   for kind in KINDS:
    p=Path(d)/kind;scaffold(kind,p);self.assertTrue((p/'v2/server.mjs').is_file());self.assertTrue((p/'v2/demos'/kind/'index.html').is_file());self.assertTrue((p/'v2/demos/shared/domain.mjs').is_file())
    if kind=='studio':self.assertTrue((p/'v2/vendor/three/LICENSE').is_file());self.assertTrue((p/'v2/vendor/gsap/LICENSE.txt').is_file())
    with self.assertRaises(ValueError):scaffold(kind,p)
 def test_installer_is_non_destructive_and_complete(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'skills';p.mkdir();old=p/'awwwards-enterprise';old.mkdir();(old/'user.txt').write_text('preserve me')
   out=install(p);self.assertEqual(len(out),24);self.assertEqual(sum(x['status']=='installed' for x in out),23);self.assertEqual((old/'user.txt').read_text(),'preserve me');self.assertFalse((old/'SKILL.md').exists());self.assertTrue((p/'awwwards-fintech/PACKAGE_LOCATION.json').is_file());self.assertTrue(all(x['status']=='skipped_existing' for x in install(p)))
 def test_installer_rejects_in_package_destination(self):
  with self.assertRaises(ValueError):install(R/'v2/should-not-write')
 def test_reference_needs_rights_and_observation_evidence(self):
  ref=json.loads((R/'v2/contracts/reference-brief.example.json').read_text(encoding='utf-8'));self.assertEqual(validate('reference',ref),[]);ref['source']['permission']='';self.assertTrue(validate('reference',ref));ref['source']['permission']='authorized';ref['observations'][0]['evidence']='';self.assertTrue(validate('reference',ref))
 def test_passed_acceptance_requires_real_in_scope_evidence(self):
  c={'checks':[{'id':'x','status':'passed','method':'browser','environment':'test','evidence':['v2/contracts/asset-register.json']}]};self.assertEqual(validate('acceptance',c),[]);c['checks'][0]['evidence']=['../../missing'];self.assertTrue(validate('acceptance',c));c['checks'][0]['evidence']=[];self.assertTrue(validate('acceptance',c))
 def test_blocked_needs_reason_and_not_run_is_valid(self):
  self.assertTrue(validate('acceptance',{'checks':[{'id':'x','status':'blocked'}]}));self.assertEqual(validate('acceptance',{'checks':[{'id':'x','status':'not_run'}]}),[])
if __name__=='__main__':unittest.main(verbosity=2)
