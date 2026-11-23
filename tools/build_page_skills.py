#!/usr/bin/env python3
"""Build standalone page skills from authored recipes and measured references."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,shutil,html
from page_research import family
from reviewed_family import load_reviews,assign_family
R=Path(__file__).resolve().parents[1]
def definitions():
 spec=importlib.util.spec_from_file_location('page_definitions',R/'page_skills/definitions.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module.PAGES
def write(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8',newline='\n')
def build_story_fallback():
 folder=R/'page_skills/creative/story';data_file=folder/'story-data.json';data_file.stat();chapters=json.loads(data_file.read_text(encoding='utf-8'));p=folder/'index.html';text=p.read_text(encoding='utf-8');start='<!-- STATIC_STORY_START -->';end='<!-- STATIC_STORY_END -->'
 content='<p id="reader-enhancement-status" role="status">The complete story is available below. JavaScript enables optional reader controls.</p><section id="static-story" aria-labelledby="static-story-title"><h2 id="static-story-title">Read all three chapters</h2>'
 for i,c in enumerate(chapters,1):content+='<article id="chapter-'+str(i)+'" tabindex="-1"><h3>'+html.escape(c['title'])+'</h3>'+''.join('<h4>'+html.escape(h)+'</h4><p>'+html.escape(t)+'</p>' for h,t in c['panels'])+'</article>'
 content+='</section>';text=text[:text.index(start)+len(start)]+content+text[text.index(end):];write(p,text)

def build_editorial_fallback():
 folder=R/'page_skills/editorial/magazine';p=folder/'articles.json'
 if not p.exists():return
 data=json.loads(p.read_text(encoding='utf-8'));e=html.escape;topics={t['id']:t['label'] for t in data['topics']}
 def meta(a):
  date=a['date'];label=(str(datetime.date.fromisoformat(date).day)+' '+datetime.date.fromisoformat(date).strftime('%b %Y')) if date else 'Date not recorded'
  return ('<time datetime="'+date+'">'+e(label)+'</time>' if date else '<span>'+label+'</span>')+' · '+e(a['author'])
 def card(a):
  return '<li id="card-'+a['id']+'" tabindex="-1"><article class="card"><div class="art '+a['art']+'" aria-hidden="true"></div><p class="eyebrow">'+e(topics[a['topic']])+'</p><h3><a data-story="'+a['id']+'" href="#story-'+a['id']+'">'+e(a['title'])+'</a></h3><p class="summary">'+e(a['summary'])+'</p><p class="meta">'+meta(a)+'</p><a class="read" aria-label="Read story: '+e(a['title'])+'" data-story="'+a['id']+'" href="#story-'+a['id']+'">Read story</a></article></li>'
 articles=sorted(data['articles'],key=lambda a:(a['date'] or '',a['id']),reverse=True);feature=next(a for a in articles if a['id']==data['featured'])
 featured='<div class="art '+feature['art']+'" aria-hidden="true"></div><div><p class="eyebrow">Featured / '+e(topics[feature['topic']])+'</p><h2>'+e(feature['title'])+'</h2><p>'+e(feature['summary'])+'</p><p class="note">'+meta(feature)+'</p><a class="read" data-story="'+feature['id']+'" href="#story-'+feature['id']+'">Read the featured story</a></div>'
 stories=''.join('<article class="static-story" id="story-'+a['id']+'" tabindex="-1"><h3>'+e(a['title'])+'</h3><p class="meta">'+e(topics[a['topic']])+' / '+meta(a)+'</p>'+''.join('<p>'+e(text)+'</p>' for text in a['body'])+'<a href="#catalog">Back to the story index</a></article>' for a in articles)
 p=folder/'index.html';text=p.read_text(encoding='utf-8')
 for key,value in [('FEATURED',featured),('CATALOG',''.join(card(a) for a in articles)),('STORIES',stories)]:
  start='<!-- '+key+'_START -->';end='<!-- '+key+'_END -->';text=text[:text.index(start)+len(start)]+value+text[text.index(end):]
 write(p,text)

def generate():
 build_story_fallback()
 build_editorial_fallback()
 static_file=R/'page_skills/business/collection/render_static.py';spec=importlib.util.spec_from_file_location('collection_static',static_file);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.render(static_file.parent)
 source_file=R/'research/live_pages/sources.jsonl';sources=[];reviews=load_reviews(R)
 if source_file.exists():
  with source_file.open(encoding='utf-8') as f:
   for line in f:
    if line.strip():
     source=json.loads(line);assignment=assign_family(source,reviews);source['family']=assignment['family'];sources.append(source)
 visual_file=R/'research/live_pages/visual-observations.json';visual=json.loads(visual_file.read_text(encoding='utf-8')).get('observations',[]) if visual_file.exists() else []
 patterns=json.loads((R/'interaction_skills/registry.json').read_text(encoding='utf-8'))['skills']
 creative_file=R/'research/live_pages/creative-page-observations.json';creative=json.loads(creative_file.read_text(encoding='utf-8')).get('observations',[]) if creative_file.exists() else []
 business_file=R/'research/live_pages/pricing-page-observations.json';creative+=json.loads(business_file.read_text(encoding='utf-8')).get('observations',[]) if business_file.exists() else []
 editorial_file=R/'research/live_pages/editorial-page-observations.json';creative+=json.loads(editorial_file.read_text(encoding='utf-8')).get('observations',[]) if editorial_file.exists() else []
 product_file=R/'research/live_pages/product-page-observations.json';creative+=json.loads(product_file.read_text(encoding='utf-8')).get('observations',[]) if product_file.exists() else []
 collection_file=R/'research/live_pages/collection-page-observations.json';creative+=json.loads(collection_file.read_text(encoding='utf-8')).get('observations',[]) if collection_file.exists() else []
 registry=[]
 for id,families,title,kind,regions,workflow,fields,recovery,motion in definitions():
  name='awwwards-page-'+id;folder=R/'skills'/name
  observed=[s for s in sources if s['family'] in families and s['inspection_level']=='http_dom' and (kind=='notfound' or s.get('content_state_hint','unclassified')=='unclassified') and (kind=='notfound' or not any(x in s.get('title','').lower() for x in ['not found','just a moment','404']))]
  if id=='external-careers':
   observed=sorted(observed,key=lambda s:(any(x in s.get('title','').lower() for x in ['accessibility','accommodation','choose your country']),len(s['url'])))
  if id=='external-editorial-index':observed.sort(key=lambda s:(s['id'] not in ['61347083729f7876','a6e0e3d19a1ef887'],s['id']!='61347083729f7876'))
  if id=='external-pricing':observed.sort(key=lambda s:s['id']!='a955e8342ff580e5')
  if id=='external-product':observed.sort(key=lambda s:s['id']!='5be4915e232c552f')
  if id=='external-collection':observed.sort(key=lambda s:s['id']!='1c38bba0ec8fd63f')
  if id=='external-prompt-detail':observed.sort(key=lambda s:s['id']!='619b8560ee5995dd')
  selected=observed[:6];source_ids={s['id'] for s in selected};views=[v for v in visual if v['source_id'] in source_ids and v['status']=='rendered_observed']
  state_views=[v for v in creative if v['source_id'] in source_ids]
  level='rendered_source_observations' if any(v['status'] in ['rendered_content_observed','rendered_content_signals_observed','rendered_observed'] for v in state_views) else 'rendered_geometry' if views else ('http_dom' if selected else 'not_observed')
  goal={'editorial-index':'按主题和完整目录搜索发现文章，并可靠继续加载、阅读与返回。','story-index':'选择可用章节，理解阅读顺序并按需恢复已保存的位置。','story':'以明确顺序阅读当前章节，并能切换阅读方式、继续或退出。','prompt':'审阅并编辑分层提示词，理解样例来源并可靠复制原创配方。','careers':'理解雇主理念、工作方式和岗位入口，再审阅符合条件的角色。','gallery':'按主题浏览视觉作品，用可访问的查看器审阅并返回索引。','experiment':'理解输入方式并可控地体验、暂停和退出互动实验。','notfound':'理解资源不可达的原因，并通过有效入口恢复任务。','listing':'帮助用户在完整结果中定位条目，并进入详情或恢复空结果。','directory':'根据实体身份和明确筛选找到合适的对象。','portal':'让用户理解内容层级，并进入当前最重要的任务。','award':'理解作品、奖项与来源，并安全进入原站或相关内容。','pricing':'理解计费周期和权益限制，再审阅明确的方案。','wizard':'分步收集最少必要输入，在最终行动前审阅和确认。','course':'理解课程与大纲，明确公开预览和访问权限。','product':'核对产品、规格、许可与费用，完成可核实的选择。','job':'理解岗位及申请条件，进入明确的申请路径。','contact':'完成可恢复的询问表单并理解提交的实际状态。','faq':'找到相关答案，理解下一步及帮助渠道。','event':'理解活动时间、议程、地点与参与条件。','article':'按章节持续阅读并追溯事实、版本和引用。','profile':'理解身份、贡献、作品与公开联系边界。','project':'理解项目问题、过程、贡献和有证据的成果。','about':'理解主体、团队和可核实的背景。','service':'判断服务与当前问题的适配性，并进入咨询。'}[('listing' if kind=='shop-index' else kind)]
  if kind=='shop-index':goal='按明确的即时筛选与完整目录查询发现商品，并可靠继续浏览、查看信息和返回。'
  contract={'schema_version':'3.0','id':id,'skill':name,'title':title,'kind':kind,'scope':'Awwwards-linked external inner page; specific award status requires official evidence' if id.startswith('external-') else 'Awwwards main-site page family','source_families':families,'goal':goal,'regions':regions.split('、'),'workflow':workflow,'data_fields':fields,'failure_recovery':recovery,'motion_contract':motion,'evidence_level':level,'source_relationship_note':'An outbound work-detail association does not certify that every current inner page won an award or matches a historical version.','evidence_note':'Only recorded observations are facts. DOM structure does not prove visual composition, hidden state, source code, backend behavior or licenses. The runnable blueprint is an original recipe, not a source-site clone.','sources':[{'id':s['id'],'url':s['url'],'family':s['family'],'inspection_level':s['inspection_level'],'observed_at':s['observed_at'],'source_sha256':s.get('source_sha256'),'structure':s['structure']} for s in selected],'visual_metrics':views,'source_state_observations':state_views,'source_coverage':'observed_examples' if selected else 'needs_source_inspection','original_blueprint':True,'business_mode':'local_preview','states':['default','loading','empty','error','success_preview','disabled','keyboard_focus','reduced_motion','narrow_view'],'acceptance':[goal,recovery,motion,'320、390、768、1440 宽度不出现整页横溢出；必要表格在独立区域滚动。','键盘可进入、操作、关闭对话框并返回触发点；错误不只靠颜色。','本地预览不得暗示真实支付、投稿、消息、账户或预约已生效。'],'limitations':['Source interaction audit is not automatically performed','Source assets are not bundled','Real backend, production and physical-device acceptance are not included']}
  if id=='external-prompt-detail':contract['reference_eligibility_note']='The AIFont official work-detail title was Nominee at the recorded observation. This is a supplementary reference, not counted as a confirmed awarded-site case; a later live read was HTTP 403.'
  if id=='external-pricing':
   contract['estimate_contract']={'implementation':'Original fictional tariff; never source provider prices or live billing','amount_precision':'BigInt integer cents; aggregate each monthly component before half-up rounding','runtime_precision':'Milliseconds, at most three decimal places','display_basis':'Per second or per hour; changing display cannot change workload or total','unknown_fee':'Preserve null base and total for custom workspace fees; known usage remains visible','edit_policy':'Invalidate old estimate on edits; require recalculation before review','limits':{'requests':10000000,'active_seconds':3600,'accelerators':8,'vcpus':64,'memory_gb':256,'storage_gb':100000},'excluded_costs':['Tax','Transfer','Idle allocation','Discounts and commitments','Currency conversion']}
   contract['acceptance']+=['单位切换不改变工作量或月度总额；月费与存储始终按月标记。','小数不可静默删除或重新解释；错误可编辑恢复，旧估算在输入变化后失效。','比较套餐与估算套餐独立；断点变化不能让焦点留在隐藏内容。','未知月费不得显示为零或已知总额；无脚本和数据失败仍可读全部套餐与静态示例。']
  if id=='external-editorial-index':
   contract['editorial_contract']={'demo_catalog':'Twelve original fictional stories, authors and CSS illustrations','query_scope':'Entire local catalog, including full story text; not just loaded cards','paging':'Versioned query-bound cursors; confirmed total is distinct from a request failure','stale_request_policy':'Abort previous requests and ignore obsolete responses','reading_return':'Preserve topic, query, order, expanded position, origin focus and scroll','fallback':'Complete pre-rendered original catalog, all story text and native destinations','data_editing':'Regenerate the static fallback whenever articles.json changes','limits':'Catalog parser is bounded; twenty-record paging is tested, while large-catalog production performance is not accepted','source_api_reproduction':False,'source_media_redistributed':False}
   contract['acceptance']+=['加载更多保留现有条目且不重复；失败重试同一游标，旧筛选结果不能覆盖新筛选。','阅读与返回恢复查询、主题、排序、已展开位置和触发焦点；页内锚点不应误触查询刷新。','无脚本或资源失败时可读取全部原创目录与完整正文；原文地址不可达时有有效恢复入口。','同名源站控件必须唯一定位或核对已观察的目标地址；不能默认把第一个匹配当作预期交互。']
  if id=='external-product':
   contract['product_contract']={'implementation':'Original fictional lamp, text, CSS illustrations, stock and integer-cent local estimates','gallery':'Three explicit views; no autoplay; enlarged dialog supports arrows and focus return','selection':'Labeled native color radios, size selector and express checkbox; unknown and sold-out stock remain distinct','estimate':'Edits invalidate old estimates and abort pending work; a new estimate is required before review','unknown_fees':'Known subtotal and express fee only; tax, delivery and final payable total remain null','source_field_review':'Inspect visible labels and custom controls as well as native visibility; an empty native-visible list does not prove absence','family_review':'Exact URL review is tied to the metadata hash and becomes stale after source changes','not_reproduced':['Real cart, wishlist, orders or payment','Source color switching: only one option observed','Source price recalculation','Source autoplay','Cartier configurator, blocked with HTTP403']}
   contract['acceptance']+=['图库切换、放大、方向键和关闭后的焦点返回必须实际操作；不自动轮播。','颜色与加急选项具有可见标签，未知库存与售罄不能伪造为可购买。','数量不接受空值、小数或指数；整数金额展示与计算一致，未知税费、配送和最终应付金额保持未知。','编辑使旧估算失效，取消中的旧响应不能覆盖新选择；失败重试保留输入。','无脚本或产品数据失败时保留全部原创视图、价格示例和规格；真实后端与源站素材不随模板交付。']
  if id=='external-collection':
   contract['collection_contract']={'implementation':'Eighteen original fictional objects with CSS illustrations, complete static descriptions and local asynchronous queries','filter_timing':'Live: selection triggers query while drawer remains open; Show objects closes without discarding confirmed filters','query_scope':'Full original catalog, not just currently loaded cards; OR within category, AND across dimensions','facet_counts':'Each dimension excludes its own selection while respecting search and other dimensions','confirmed_state':'URL and counts represent confirmed results; failure preserves previous confirmed cards and offers retry or restore','cursor':'Bound to catalog content revision and normalized query; not an authorization token','unknown_values':'Unknown price stays null and sorts after known prices in both directions; availability unknown is distinct from unavailable','reading_return':'Restore query, sort, shown position, origin focus and scroll','static_editing':'After catalog.json edits, run python render_static.py in the exported template and repeat validation','source_boundaries':['Reported source counts are not a full stock audit','Normal query-result read POST was permitted only for native anonymous filter UI; other POSTs remained blocked','Source pagination, exhaustive combinations and purchase states untested']}
   contract['acceptance']+=['即时筛选不等待关闭才更新；Esc/关闭保留已确认选择，显示结果后有明确焦点落点。','数量来自完整查询；失败不可冒充空结果，待定选择与已确认结果有可读区分。','同类多选 OR、维度之间 AND；选项数量口径明确，过期响应不能覆盖较新筛选。','加载更多保留卡片与游标；返回商品列表恢复查询、排序、展开位置与触发焦点。','无脚本与数据失败保留全部原创商品信息；价格未知不显示为零，原站资产与真实库存不随包交付。']
  write(folder/'references/page-contract.json',json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
  source_list='\n'.join('- '+s['url']+'（'+s['inspection_level']+'；'+s['observed_at']+'）' for s in selected) or '- 本轮尚未读取到该页面族的完整来源。保持 needs_source_inspection；不得声称已从原站提炼完整设计。'
  text=f'''---
name: {name}
description: Design and implement a {id.replace('-', ' ')} page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# {title}

## 适用任务
{goal} 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `{level}`；页面族覆盖 `{contract['source_coverage']}`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：{regions}。
'''+''.join(f'{i}. {step}\n' for i,step in enumerate(workflow,1))+f'''
## 数据与状态
字段：{', '.join(fields)}。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：{recovery}

## 动效与响应式
{motion} 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

## 可运行原创蓝本
`assets/` 包含独立 HTML/CSS/JS 与契约，不需要 npm 或第三方素材。导出到用户指定的空目录：
```text
python scripts/scaffold.py --output YOUR_EMPTY_PROJECT_DIRECTORY
```
进入导出目录运行 `python -m http.server 8000 --bind 127.0.0.1`，打开 http://127.0.0.1:8000/ 。file:// 不能加载 JSON 模块。已有项目按契约移植，不直接覆盖用户代码。

蓝本使用虚构数据和明确本地预览状态。它示范区域、交互与恢复，不意味着按像素复刻原站，也不包含真实业务接口。看见按钮后必须操作测试；静态检查不能代替浏览器证据。

## 验收与交付
交付路由/组件边界、状态矩阵、数据契约、来源和素材台账、实际运行命令、截图及未测项。检查契约中的每条 acceptance，记录 passed/failed/blocked/not_run 并给出证据。不要从一个测试通过推断整站、全部设备或生产已验收。

## 已读取的来源
{source_list}

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。
'''
  companions=[x['skill'] for x in patterns if name in x['supports_page_skills']]
  if companions:text+='\n## 可组合的具体机制\n'+''.join('- `'+x+'`：读取其机制契约和实际测试边界后按需组合。\n' for x in companions)
  if id=='external-pricing':text+='\n## 定价专项实施\n读取 `assets/pricing-model.mjs` 和契约中的 `estimate_contract`。它们是独立原创虚构费率模型，不是源站计费实现。以整数金额汇总和舍入，明确单位、输入精度、未知费用和旧估算失效。源站小数输入的具体观察不能被当成建议规则。按这些边界操作所有核心路径，再接真实服务端费率和购买接口。\n'
  if id=='external-editorial-index':text+='\n## 杂志索引专项\n读取 `assets/catalog.mjs`、`assets/articles.json` 和契约中的 `editorial_contract`。示例使用独立原创全文和本地异步分页适配器，不复刻源站后端。编辑数据后重新生成完整静态正文；移植到真实服务时保留服务端完整查询、游标版本、已确认数量和失败状态。来源只观察了有限主题与加载动作，不代表所有文章已审阅。\n'
  if id=='external-product':text+='\n## 商品详情专项\n读取 `assets/product-model.mjs`、`assets/product.json` 和契约中的 `product_contract`。先区分详情与集合页，再核查图库、变体、加急选项、库存和说明折叠。源站透明原生控件可能有可见标签；实际点击已核查标签，不用强制修改隐藏 select 代替用户路径。当前来源只有一种颜色，加急勾选和准备时间的变化已观察；未证明颜色切换或源站价格重算。蓝本为独立原创虚构灯具，保留未知费用、失效估算、售罄和失败恢复；不包含真实购物接口。\n'
  if id=='external-collection':text+='\n## 商品集合专项\n读取 `assets/catalog.mjs`、`assets/catalog.json` 及 `collection_contract`。蓝本采用即时查询：更改选项即更新结果，关闭抽屉保留已确认过滤。它是独立原创虚构目录，不复刻源站数据或后端。移植真实服务时保持已确认数量、未知价格、游标版本、失败恢复及列表返回。编辑 JSON 后运行模板内 `python render_static.py` 更新完整静态目录，再测试所有主路径。源站报告数量和单次查询响应不等于全部库存或所有组合已验收。\n'
  write(folder/'SKILL.md',text)
  write(folder/'assets/contract.json',json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
  write(folder/'assets/index.html','<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Original task-specific page skill blueprint with fictional local data."><title>'+id+' · Page skill blueprint</title><link rel="icon" href="data:,"><link rel="stylesheet" href="style.css"></head><body><a class="skip" href="#main">Skip to content</a><div id="app"><main id="main"><h1>Original page skill blueprint</h1><p>Read the page contract for the structure, states and source boundaries. JavaScript enables the local interaction example.</p></main></div><noscript>Interactive local previews require JavaScript. The page contract and skill instructions remain readable.</noscript><script type="module" src="main.mjs"></script></body></html>')
  shutil.copy2(R/'page_skills/runtime.css',folder/'assets/style.css');shutil.copy2(R/'page_skills/runtime.mjs',folder/'assets/main.mjs')
  write(folder/'scripts/scaffold.py','''#!/usr/bin/env python3
from pathlib import Path
import argparse,shutil,json
source=Path(__file__).resolve().parents[1]/'assets'
def scaffold(output):
 target=Path(output).expanduser().resolve()
 if target==source or source in target.parents:raise ValueError('Choose a directory outside skill assets')
 if target.exists() and any(target.iterdir()):raise ValueError('Refusing to overwrite a nonempty directory')
 target.mkdir(parents=True,exist_ok=True)
 for p in source.iterdir():shutil.copy2(p,target/p.name)
 return {'output':str(target),'start':'python -m http.server 8000 --bind 127.0.0.1','mode':'local_original_preview'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
 try:print(json.dumps(scaffold(a.output)))
 except (OSError,ValueError) as e:p.exit(2,str(e)+'\\n')
''')
  runtime_variant='careers-pattern' if kind=='careers' else 'generic-page'
  if kind=='careers':
   source=R/'interaction_skills/assets/careers'
   shutil.copy2(source/'index.html',folder/'assets/index.html');shutil.copy2(source/'style.css',folder/'assets/style.css');shutil.copy2(source/'main.mjs',folder/'assets/runtime.mjs');shutil.copy2(R/'interaction_skills/page_adapter.mjs',folder/'assets/main.mjs')
  if kind in ['story','story-index','prompt']:
   runtime_variant='creative-story' if kind.startswith('story') else 'creative-prompt'
   source=R/'page_skills/creative'/('story' if kind.startswith('story') else 'prompt')
   for source_file in source.iterdir():
    if source_file.is_file():shutil.copy2(source_file,folder/'assets'/source_file.name)
  if id=='external-editorial-index':
   runtime_variant='editorial-magazine';source=R/'page_skills/editorial/magazine'
   for source_file in source.iterdir():
    if source_file.is_file():shutil.copy2(source_file,folder/'assets'/source_file.name)
  if id=='external-pricing':
   runtime_variant='business-pricing';source=R/'page_skills/business/pricing'
   for source_file in source.iterdir():
    if source_file.is_file():shutil.copy2(source_file,folder/'assets'/source_file.name)
  if id=='external-product':
   runtime_variant='business-product';source=R/'page_skills/business/product'
   for source_file in source.iterdir():
    if source_file.is_file():shutil.copy2(source_file,folder/'assets'/source_file.name)
  if id=='external-collection':
   runtime_variant='business-collection';source=R/'page_skills/business/collection'
   for source_file in source.iterdir():
    if source_file.is_file():shutil.copy2(source_file,folder/'assets'/source_file.name)
  registry.append({'id':id,'skill':name,'title':title,'kind':kind,'runtime_variant':runtime_variant,'source_families':families,'source_coverage':contract['source_coverage'],'source_count':len(selected),'evidence_level':level,'path':folder.relative_to(R).as_posix(),'demo':folder.relative_to(R).as_posix()+'/assets/','browser_validation':'See validation evidence; not inferred from generation'})
 out={'schema_version':'3.0','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'core_skills_preserved':24,'page_skills':len(registry),'status':'in_progress','scope':'Awwwards main pages and awarded external-site inner pages, organized into reusable task-specific skills','not_claimed':['All pages visited','All awarded websites fully analyzed','All source interactions reproduced'],'skills':registry}
 write(R/'page_skills/registry.json',json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'page_skills':len(registry),'observed_page_families':sum(x['source_coverage']=='observed_examples' for x in registry),'requires_source_inspection':sum(x['source_coverage']!='observed_examples' for x in registry)},ensure_ascii=True));return out
if __name__=='__main__':generate()
