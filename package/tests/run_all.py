#!/usr/bin/env python3
"""Self-contained reproducibility smoke suite; source data is NOT reverified against live websites."""
import json,subprocess,sys,tempfile,shutil
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1]; tests=[]

def run(name,args,expected=0):
 try:
  p=subprocess.run([str(x) for x in args],capture_output=True,text=True,timeout=30,cwd=R)
  passed=p.returncode==expected
  tests.append({'name':name,'status':'passed' if passed else 'failed','expected_exit':expected,'actual_exit':p.returncode,'stderr':p.stderr[-500:] if not passed else ''})
  return passed
 except Exception as e:
  tests.append({'name':name,'status':'blocked','error':str(e)});return False

def write(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
PY=sys.executable
run('archive_validate',[PY,'skills/awwwards-research/scripts/archive_tool.py','validate'])
run('case_citations_validate',[PY,'skills/awwwards-reference/scripts/case_tool.py','validate'])
run('motion_spec',[PY,'skills/awwwards-motion/scripts/check_motion_spec.py','skills/awwwards-motion/examples/motion-spec.json'])
run('webgl_spec',[PY,'skills/awwwards-webgl/scripts/check_scene_spec.py','skills/awwwards-webgl/examples/scene-spec.json'])
run('webgl_resource_scope',['node','skills/awwwards-webgl/scripts/test_resource_scope.mjs'])
run('content_contract',[PY,'skills/awwwards-content/scripts/audit_content.py','skills/awwwards-content/examples/site-content.json'])
run('ux_flow_contract',[PY,'skills/awwwards-product-ux/scripts/validate_flow.py','skills/awwwards-product-ux/examples/demo-request-flow.json'])
run('six_templates_scaffold_static',[PY,'skills/awwwards-components/scripts/static_self_test.py'])
run('metrics_not_run_cannot_pass',[PY,'skills/awwwards-quality/scripts/check_budget.py','skills/awwwards-quality/examples/metric-result.json'],expected=2)
archive=json.loads((R/'research/archive/sites_of_the_month.json').read_text(encoding='utf-8'))
cases=json.loads((R/'research/cases/representative_30.json').read_text(encoding='utf-8'))
tests.append({'name':'archive_case_counts','status':'passed' if len(archive['rows'])==206 and len(cases['cases'])==30 else 'failed','archive':len(archive['rows']),'cases':len(cases['cases'])})
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp)
 for preset in ['fintech','editorial','playful']:
  out=t/preset;run(f'tokens_build_{preset}',[PY,'skills/awwwards-design-system/scripts/make_tokens.py','--preset',preset,'--output',out]);run(f'tokens_contrast_{preset}',[PY,'skills/awwwards-design-system/scripts/validate_tokens.py',out/'design-tokens.json'])
  if preset=='fintech':
   d=json.loads((out/'design-tokens.json').read_text(encoding='utf-8'));d['colors']['text']='#172b35';bad=t/'low-contrast.json';write(bad,d)
   run('negative_low_contrast_rejected',[PY,'skills/awwwards-design-system/scripts/validate_tokens.py',bad],expected=1)
 project=t/'project';run('project_initializer',[PY,'skills/awwwards-workflow/scripts/init_project.py','--goal','测试SaaS','--kind','saas','--output',project]);run('project_validator_unverified_status',[PY,'skills/awwwards-workflow/scripts/validate_stage.py','--project',project]);run('negative_no_overwrite_project',[PY,'skills/awwwards-workflow/scripts/init_project.py','--goal','测试SaaS','--kind','saas','--output',project],expected=2)
 spec=json.loads((project/'stages/research.json').read_text(encoding='utf-8'));spec['status']='passed';write(project/'stages/research.json',spec)
 run('negative_stage_without_evidence_rejected',[PY,'skills/awwwards-workflow/scripts/validate_stage.py','--project',project],expected=1)
 layout=t/'layout.json';run('layout_spec_creation',[PY,'skills/awwwards-layout/scripts/prepare_layout.py','--kind','saas','--output',layout])
 prod=t/'saas';run('scaffold_saas',[PY,'skills/awwwards-components/scripts/scaffold.py','--kind','saas','--name','测试','--output',prod]);run('negative_no_overwrite_scaffold',[PY,'skills/awwwards-components/scripts/scaffold.py','--kind','saas','--name','测试','--output',prod],expected=2)
 for kind in ('saas','commerce','dashboard','portfolio','editorial','immersive'):
  run(f'example_html_{kind}',[PY,'skills/awwwards-quality/scripts/static_audit.py',R/'examples'/kind/'index.html'])
  run(f'example_js_syntax_{kind}',['node','--check',R/'examples'/kind/'main.js'])
 run('shared_js_syntax',['node','--check','skills/awwwards-components/templates/shared/common.js'])
 write(t/'valid_measured.json',{'status':'measured','source':'fictional test fixture (NOT real measurement)','measured_at':'2026-01-01T00:00:00Z','device':'test-fixture','percentile':75,'sample_count':1,'lcp_ms':1500,'inp_ms':120,'cls':0.04})
 run('synthetic_budget_parser_unit_test',[PY,'skills/awwwards-quality/scripts/check_budget.py',t/'valid_measured.json'])
 write(t/'invalid_flow.json',{'mode':'production','user_goal':'pay','primary_action':'Pay','states':['idle','loading','success','error'],'transitions':[],'operation':'payment'})
 run('negative_fake_payment_rejected',[PY,'skills/awwwards-product-ux/scripts/validate_flow.py',t/'invalid_flow.json'],expected=1)
 write(t/'invalid_content.json',{'site_name':'test','routes':[{'path':'/','title':'hello','description':'Lorem ipsum','h1':'hello','primary_cta':'test','public_claims':[{'text':'100 customers'}]}]})
 run('negative_unsourced_claim_rejected',[PY,'skills/awwwards-content/scripts/audit_content.py',t/'invalid_content.json'],expected=1)
 incoming=t/'incoming.json';write(incoming,[{'id':'original-case','name':'Original Case','official_url':'https://www.awwwards.com/sites/original-case','source_url':'https://www.awwwards.com/websites/sites_of_the_month/','retrieved_at':'2026-11-23','award_year':2026,'award_month':None}]);run('nondestructive_archive_merge',[PY,'skills/awwwards-research/scripts/merge_archive.py','--incoming',incoming,'--output',t/'archive-new.json'])
 run('nonempty_archive_merge_cannot_overwrite',[PY,'skills/awwwards-research/scripts/merge_archive.py','--incoming',incoming,'--output',t/'archive-new.json'],expected=2)
 result=(R/'tests/package-test-results.json')
 report={'test_date':datetime.now(timezone.utc).isoformat(),'method':'Python/Node CLI and static example checks; online research and real-user CWV not rerun. Synthetic fixture checks exercise parser only.','status':'passed' if all(x['status']=='passed' for x in tests) else 'failed','tested':len(tests),'passed':sum(x['status']=='passed' for x in tests),'failed':[x for x in tests if x['status']!='passed'],'tests':tests,'browser':'See tests/offline-dom-results.json for 12 Chromium set_content DOM/layout/behavior tests; no HTTP/module-loader/CWV testing.'}
 result.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'status':report['status'],'tested':len(tests),'passed':report['passed'],'failed':report['failed']},ensure_ascii=False,indent=2))
 sys.exit(0 if report['status']=='passed' else 1)
