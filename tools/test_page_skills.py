#!/usr/bin/env python3
import hashlib,html,importlib.util,json,sys,tempfile,unittest
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from page_research import normalize,Robots,Structure,Collector,family,content_state_hint
from build_page_skills import definitions
from reviewed_family import load_reviews,assign_family
from install_all_skills import install
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class PageSkills(unittest.TestCase):
 def test_reference_static_content_preserves_media_transcript_and_all_original_notes(self):
  import shutil
  with tempfile.TemporaryDirectory() as t:
   target=Path(t)/'reference';shutil.copytree(R/'page_skills/editorial/reference',target)
   p=target/'reference.json';d=json.loads(p.read_text(encoding='utf-8'));d['title']='<Reference fixture>';p.write_text(json.dumps(d),encoding='utf-8')
   result=load(target/'render_static.py','reference_static_fixture').render(target);self.assertEqual(result,{'transcript_segments':3,'related_notes':3})
   text=(target/'index.html').read_text(encoding='utf-8');self.assertIn('&lt;Reference fixture&gt;',text);self.assertIn(hashlib.sha256(p.read_bytes()).hexdigest(),text);self.assertEqual(text.count('class="reading"'),3);self.assertIn('captions.vtt',text);self.assertIn('controls playsinline muted',text);self.assertNotIn('<video autoplay',text);self.assertIn(html.escape(d['summary']),text);self.assertIn(html.escape(d['creator']),text)
   for note in d['related']:self.assertIn(html.escape(note['body']),text)
 def test_reference_review_is_main_site_detail_and_not_the_external_experience(self):
  reviews=load_reviews(R);review=reviews['https://www.awwwards.com/inspiration/20-years-of-xbox-museum-timeline'];source={'url':review['url'],'id':review['source_id'],'source_sha256':review['source_sha256'],'inspection_level':'http_dom'}
  self.assertEqual(assign_family(source,reviews)['family'],'main.inspiration-detail');source['source_sha256']='0'*64;self.assertEqual(assign_family(source,reviews)['review_status'],'stale')
 def test_technical_static_regeneration_updates_digest_and_preserves_four_sections(self):
  import shutil
  with tempfile.TemporaryDirectory() as t:
   target=Path(t)/'technical';shutil.copytree(R/'page_skills/business/technical',target)
   p=target/'product.json';d=json.loads(p.read_text(encoding='utf-8'));d['title']='<Folio fixture>';d['dimensions']['depth_mm']=None;p.write_text(json.dumps(d),encoding='utf-8')
   module=load(target/'render_static.py','technical_static_fixture');self.assertEqual(module.render(target)['panels'],4)
   text=(target/'index.html').read_text(encoding='utf-8');self.assertEqual(text.count('class="panel"'),4);self.assertIn('&lt;Folio fixture&gt;',text);self.assertIn(hashlib.sha256(p.read_bytes()).hexdigest(),text);self.assertIn('Not supplied',text)
   sheet=(target/'concept-sheet.txt').read_text(encoding='utf-8');self.assertIn('LAYOUTS',sheet);self.assertIn('Fire classification: Not verified',sheet)
 def test_technical_review_corrects_only_the_reviewed_product_url(self):
  reviews=load_reviews(R);review=reviews['https://fluid.glass/collection/fluid-folding-door'];source={'url':review['url'],'id':review['source_id'],'source_sha256':review['source_sha256'],'inspection_level':'http_dom'}
  result=assign_family(source,reviews);self.assertEqual(result['family'],'external.technical-product');self.assertEqual(result['heuristic'],'external.collection')
  source['url']='https://fluid.glass/collection/another';self.assertEqual(assign_family(source,reviews)['family'],'external.collection')
 def test_shop_collection_and_product_candidates_are_separate(self):
  for url in ['https://example.com/shop/','https://example.com/products/','https://example.com/en/collections','https://example.com/collections/lighting?page=2','https://example.com/product-category/lamps']:
   self.assertEqual(family(url),'external.collection')
  for url in ['https://example.com/products/arc','https://example.com/collections/lighting/products/arc']:
   self.assertEqual(family(url),'external.product')
 def test_collection_static_generator_preserves_complete_original_information(self):
  folder=R/'page_skills/business/collection';data=json.loads((folder/'catalog.json').read_text(encoding='utf-8'));markup=(folder/'index.html').read_text(encoding='utf-8')
  for p in data['products']:
   self.assertIn('id="object-'+p['id']+'"',markup);self.assertIn('href="#object-'+p['id']+'"',markup);self.assertIn(html.escape(p['detail']),markup);self.assertIn(html.escape(p['description']),markup)
  renderer=load(folder/'render_static.py','collection_static_test')
  with tempfile.TemporaryDirectory() as d:
   temp=Path(d)
   for name in ['index.html','catalog.json']:(temp/name).write_bytes((folder/name).read_bytes())
   changed=json.loads((temp/'catalog.json').read_text(encoding='utf-8'));changed['products'][0]['title']='Edited <original>';changed['products'][0]['price_cents']=12345;(temp/'catalog.json').write_text(json.dumps(changed),encoding='utf-8');self.assertEqual(renderer.render(temp),18);text=(temp/'index.html').read_text(encoding='utf-8');self.assertIn('Edited &lt;original&gt;',text);self.assertIn('$123.45 USD',text)
 def test_exact_url_review_assigns_arbitrary_slug_without_generalizing(self):
  reviews=load_reviews(R)
  with (R/'research/live_pages/sources.jsonl').open(encoding='utf-8') as f:
   source=next(json.loads(line) for line in f if '5be4915e232c552f' in line)
  assigned=assign_family(source,reviews);self.assertEqual(assigned['family'],'external.product');self.assertEqual(assigned['heuristic'],'external.other')
  self.assertEqual(assign_family({**source,'url':'https://marryandbride.com/a-different-slug/'},reviews)['family'],'external.other')
 def test_review_becomes_stale_when_cached_source_hash_changes_or_source_is_unavailable(self):
  reviews=load_reviews(R);review=next(iter(reviews.values()));source={'url':review['url'],'id':review['source_id'],'source_sha256':review['source_sha256'],'inspection_level':'http_dom'}
  for changed in [{**source,'source_sha256':'0'*64},{**source,'inspection_level':'http_error'},{**source,'id':'other'}]:
   result=assign_family(changed,reviews);self.assertEqual(result['review_status'],'stale');self.assertEqual(result['family'],'external.other')
 def test_product_static_fallback_has_all_views_prices_and_disabled_selection_controls(self):
  text=(R/'page_skills/business/product/index.html').read_text(encoding='utf-8')
  for part in ['data-view="0"','data-view="1"','data-view="2"','$145.00','$185.00','id="configuration" disabled','Tax and delivery are unknown']:
   self.assertIn(part,text)
 def test_editorial_static_fallback_keeps_every_original_story_and_native_destination(self):
  folder=R/'page_skills/editorial/magazine';data=json.loads((folder/'articles.json').read_text(encoding='utf-8'));markup=(folder/'index.html').read_text(encoding='utf-8')
  for article in data['articles']:
   self.assertIn('id="story-'+article['id']+'"',markup);self.assertIn('href="#story-'+article['id']+'"',markup)
   for paragraph in article['body']:self.assertIn(html.escape(paragraph),markup)
 def test_editorial_indexes_topics_and_article_candidates_remain_distinct(self):
  for url in ['https://apinistudio.com/blogs/notizie','https://apinistudio.com/blogs/notizie/tagged/bespoke','https://www.emilynixon.com/blogs/b-66/','https://example.com/en/journal','https://example.com/blog/page/2','https://example.com/magazine/']:
   self.assertEqual(family(url),'external.editorial-index')
  for url in ['https://apinistudio.com/blogs/notizie/introducing-apini-bespoke','https://example.com/journal/a-story']:
   self.assertEqual(family(url),'external.article')
  self.assertEqual(family('https://example.com/bloggers'),'external.other')
 def test_pricing_page_candidates_keep_localized_inner_page_identity(self):
  for url in ['https://example.com/pricing','https://example.com/en/pricing','https://example.com/plans/team']:
   self.assertEqual(family(url),'external.pricing')
  self.assertEqual(family('https://example.com/pricing-guide'),'external.other')
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
