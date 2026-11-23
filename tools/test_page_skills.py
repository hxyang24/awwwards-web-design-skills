#!/usr/bin/env python3
import hashlib,importlib.util,json,sys,tempfile,unittest
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from page_research import normalize,Robots,Structure,Collector,family,content_state_hint
from build_page_skills import definitions
from install_all_skills import install
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class PageSkills(unittest.TestCase):
 def test_each_authored_skill_is_standalone_and_exports_without_overwriting(self):
  registry=json.loads((R/'page_skills/registry.json').read_text(encoding='utf-8'));self.assertEqual(len(registry['skills']),len(definitions()))
  with tempfile.TemporaryDirectory() as d:
   for row in registry['skills']:
    folder=R/row['path'];self.assertIn('name: '+row['skill'],(folder/'SKILL.md').read_text(encoding='utf-8'))
    module=load(folder/'scripts/scaffold.py',row['id']);out=Path(d)/row['id'];module.scaffold(out)
    for name in ['index.html','style.css','main.mjs','contract.json']:self.assertTrue((out/name).is_file())
    expected={p.relative_to(folder/'assets').as_posix() for p in (folder/'assets').rglob('*') if p.is_file()};self.assertEqual(expected,{p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()})
    for relative in expected:
     with (folder/'assets'/relative).open('rb') as f:a=hashlib.file_digest(f,'sha256').hexdigest()
     with (out/relative).open('rb') as f:b=hashlib.file_digest(f,'sha256').hexdigest()
     self.assertEqual(a,b)
    before=(out/'contract.json').read_bytes()
    with self.assertRaises(ValueError):module.scaffold(out)
    self.assertEqual((out/'contract.json').read_bytes(),before)
 def test_observed_skill_claims_resolve_to_real_source_observations(self):
  source={r['id']:r for r in [json.loads(line) for line in (R/'research/live_pages/sources.jsonl').read_text(encoding='utf-8').splitlines()]}
  for row in json.loads((R/'page_skills/registry.json').read_text(encoding='utf-8'))['skills']:
   c=json.loads((R/row['path']/'references/page-contract.json').read_text(encoding='utf-8'));self.assertEqual(c['sources'],json.loads((R/row['path']/'assets/contract.json').read_text(encoding='utf-8'))['sources'])
   self.assertEqual(c['source_coverage']=='observed_examples',bool(c['sources']))
   for s in c['sources']:self.assertIn(s['id'],source);self.assertEqual(s['source_sha256'],source[s['id']]['source_sha256']);self.assertEqual(source[s['id']]['inspection_level'],'http_dom')
 def test_skills_have_domain_specific_invariants_and_no_false_business_completion(self):
  registry=json.loads((R/'page_skills/registry.json').read_text(encoding='utf-8'));seen=set()
  for row in registry['skills']:
   c=json.loads((R/row['path']/'references/page-contract.json').read_text(encoding='utf-8'));self.assertNotIn(c['skill'],seen);seen.add(c['skill']);self.assertGreaterEqual(len(c['workflow']),3);self.assertGreaterEqual(len(c['regions']),4);self.assertEqual(c['business_mode'],'local_preview');self.assertTrue(c['original_blueprint']);self.assertTrue(c['failure_recovery'])
 def test_combined_installer_preserves_existing_skill(self):
  with tempfile.TemporaryDirectory() as d:
   dest=Path(d)/'installed';dest.mkdir();old=dest/'awwwards-workflow';old.mkdir();(old/'my.txt').write_text('keep')
   rows=install(dest);expected=len(definitions())+24+json.loads((R/'interaction_skills/registry.json').read_text(encoding='utf-8'))['interaction_skills'];self.assertEqual(len(rows),expected);self.assertEqual((old/'my.txt').read_text(),'keep');self.assertFalse((old/'SKILL.md').exists());self.assertTrue((dest/'awwwards-page-library/PACKAGE_LOCATION.json').is_file());self.assertTrue(all(r['status']=='skipped_existing' for r in install(dest)))
 def test_urls_discard_tracking_and_reject_credentials_private_hosts_and_mutations(self):
  self.assertEqual(normalize('/websites/sites_of_the_day/?utm_source=x&page=2#here','https://www.awwwards.com/'),'https://www.awwwards.com/websites/sites_of_the_day/?page=2')
  for u in ['https://u:p@example.com/','http://127.0.0.1/','http://localhost/','file:///secret','https://example.com/logout','https://example.com/a.mp4']:self.assertIsNone(normalize(u,'https://www.awwwards.com/'))
 def test_robots_wildcards_end_anchors_and_specific_allow(self):
  r=Robots('User-agent: *\nDisallow: /elements/*\nDisallow: /websites/?\nDisallow: /*/votes$\nAllow: /elements/public/\nUser-agent: MSIECrawler\nDisallow: /')
  self.assertFalse(r.allowed('https://www.awwwards.com/elements/private'));self.assertFalse(r.allowed('https://www.awwwards.com/websites/?page=2'));self.assertTrue(r.allowed('https://www.awwwards.com/websites/sites_of_the_month/?page=2'));self.assertTrue(r.allowed('https://www.awwwards.com/elements/public/example'));self.assertFalse(r.allowed('https://www.awwwards.com/name/votes'));self.assertTrue(r.allowed('https://www.awwwards.com/name/votes-detail'))
 def test_robot_policy_follows_public_redirect_and_unknown_stays_unavailable(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);c=Collector(p/'state/db.sqlite',p/'public',p/'raw',interval=0);answers=iter([(301,{'Location':'https://example.com/robots.txt'},b'',False),(200,{},b'User-agent: *\nDisallow: /private/',False)]);c.request=lambda u:next(answers)
   r,proof=c.policy('http://example.com/');self.assertEqual(proof['final_url'],'https://example.com/robots.txt');self.assertFalse(r.allowed('https://example.com/private/x'));c.db.close()
 def test_discovery_prioritizes_unobserved_page_families(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);c=Collector(p/'state/db.sqlite',p/'public',p/'raw',interval=0);c.add('https://www.awwwards.com/websites/sites_of_the_day/','https://www.awwwards.com/','main',0);c.add('https://www.awwwards.com/contact-us/','https://www.awwwards.com/','main',5);c.seen['main.award-list']=100;self.assertIn('/contact-us/',c.claim()[0]);c.db.close()
 def test_new_external_site_does_not_inherit_other_sites_sampling_penalty(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);c=Collector(p/'state/db.sqlite',p/'public',p/'raw',interval=0);c.add('https://new.example/','https://www.awwwards.com/sites/new','external',1);c.add('https://old.example/work/2','https://old.example/','external',7);c.seen['external.home']=200;c.seen_on_host[('old.example','external.project')]=10;self.assertEqual(c.claim()[0],'https://new.example/');c.db.close()
 def test_host_retry_after_keeps_its_unfetched_pages_pending(self):
  import time
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);c=Collector(p/'state/db.sqlite',p/'public',p/'raw',interval=0);c.add('https://cooling.example/','https://www.awwwards.com/','external',1);c.add('https://available.example/','https://www.awwwards.com/','external',2);c.db.execute('INSERT INTO host_backoff VALUES(?,?)',('cooling.example',time.time()+60));c.db.commit();self.assertEqual(c.claim()[0],'https://available.example/');self.assertEqual(c.db.execute('SELECT state FROM queue WHERE url=?',('https://cooling.example/',)).fetchone()[0],'pending');c.db.close()
 def test_localized_inner_pages_are_not_discarded_as_generic_urls(self):
  examples={'https://x.test/en/about-us':'external.about','https://x.test/en/archive':'external.gallery','https://x.test/en/artwork/113':'external.artwork','https://x.test/privacy-policy':'external.legal','https://x.test/lab':'external.experiment','https://x.test/404':'external.not-found','https://x.test/en/dispensa/item':'external.product','https://ponpon-mania.com/chapters':'external.story-index','https://ponpon-mania.com/chapter/1':'external.story-chapter','https://aifont.ai/fonts/tagging-letters':'external.prompt-detail','https://aifont.ai/ar/fonts/tagging-letters':'external.prompt-detail'}
  for u,f in examples.items():self.assertEqual(family(u),f)
 def test_story_static_content_contains_all_original_chapters_and_deep_links(self):
  import html
  folder=R/'page_skills/creative/story';data=json.loads((folder/'story-data.json').read_text(encoding='utf-8'));markup=(folder/'index.html').read_text(encoding='utf-8')
  self.assertEqual(len(data),3)
  for i,c in enumerate(data,1):
   self.assertIn('id="chapter-'+str(i)+'"',markup)
   for h,t in c['panels']:self.assertIn(html.escape(h),markup);self.assertIn(html.escape(t),markup)
 def test_error_headings_are_hints_without_promoting_dom_to_normal_ui(self):
  self.assertEqual(content_state_hint('Studio', ['This page couldn’t load']),'possible_render_error')
  self.assertEqual(content_state_hint('A year of Studio', ['The page doesn’t exist.']),'possible_not_found')
  self.assertEqual(content_state_hint('Studio',['Unsupported browser']),'possible_compatibility_fallback')
  self.assertEqual(content_state_hint('404 ideas for a poster',['A chapter about error design']),'unclassified')
 def test_heading_hints_ignore_script_and_preserve_inline_heading_text(self):
  s=Structure();s.feed('<title>Studio</title><script>Page not found</script><h1>This page <em>couldn’t</em> load</h1>');self.assertEqual(content_state_hint(s.title,s.heading_texts),'possible_render_error')
 def test_http_404_body_is_a_readable_error_reference_not_a_normal_page(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);c=Collector(p/'state/db.sqlite',p/'public',p/'raw',interval=0);c.policy=lambda u:(Robots(''),{'policy':'no_robots_file'});c.request=lambda u:(404,{'Content-Type':'text/html'},b'<main><h1>Page not found</h1><a href="/">Home</a></main>',False)
   row=c.inspect(('https://example.com/missing','https://example.com/','external'));self.assertEqual(row['http_status'],404);self.assertEqual(row['status'],'http_not_found');self.assertEqual(row['inspection_level'],'http_dom');self.assertEqual(row['content_state_hint'],'possible_not_found');c.db.close()
 def test_structure_does_not_treat_script_text_as_observed_navigation(self):
  s=Structure();s.feed('<title>Original page</title><nav><a href="/about">About</a></nav><script>fake nav <a href="/secret">secret</a></script><main><h1>X</h1><form><input type="email"></form></main>');self.assertEqual(s.title,'Original page');self.assertEqual(s.inputs['email'],1);self.assertEqual(s.headings['h1'],1);self.assertEqual(s.links[0]['href'],'/about')
if __name__=='__main__':
 import datetime,platform
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PageSkills))
 out=R/'research/page_skill_validation';out.mkdir(parents=True,exist_ok=True)
 (out/'unit-results.json').write_text(json.dumps({'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'passed' if result.wasSuccessful() else 'failed','tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'platform':platform.system(),'python':platform.python_version(),'scope':'Standalone exports, evidence linkage, non-overwrite installation, URL/robots safety and discovery fairness'},indent=2)+'\n',encoding='utf-8',newline='\n')
 raise SystemExit(not result.wasSuccessful())
