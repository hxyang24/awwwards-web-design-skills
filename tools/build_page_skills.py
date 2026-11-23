#!/usr/bin/env python3
"""Build standalone page skills from authored recipes and measured references."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,shutil
from page_research import family
R=Path(__file__).resolve().parents[1]
def definitions():
 spec=importlib.util.spec_from_file_location('page_definitions',R/'page_skills/definitions.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module.PAGES
def write(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8',newline='\n')
def generate():
 source_file=R/'research/live_pages/sources.jsonl';sources=[]
 if source_file.exists():
  with source_file.open(encoding='utf-8') as f:
   for line in f:
    if line.strip():
     source=json.loads(line);source['family']=family(source['url']);sources.append(source)
 visual_file=R/'research/live_pages/visual-observations.json';visual=json.loads(visual_file.read_text(encoding='utf-8')).get('observations',[]) if visual_file.exists() else []
 patterns=json.loads((R/'interaction_skills/registry.json').read_text(encoding='utf-8'))['skills']
 creative_file=R/'research/live_pages/creative-page-observations.json';creative=json.loads(creative_file.read_text(encoding='utf-8')).get('observations',[]) if creative_file.exists() else []
 registry=[]
 for id,families,title,kind,regions,workflow,fields,recovery,motion in definitions():
  name='awwwards-page-'+id;folder=R/'skills'/name
  observed=[s for s in sources if s['family'] in families and s['inspection_level']=='http_dom' and (kind=='notfound' or not any(x in s.get('title','').lower() for x in ['not found','just a moment','404']))]
  if id=='external-careers':
   observed=sorted(observed,key=lambda s:(any(x in s.get('title','').lower() for x in ['accessibility','accommodation','choose your country']),len(s['url'])))
  if id=='external-prompt-detail':observed.sort(key=lambda s:s['id']!='619b8560ee5995dd')
  selected=observed[:6];source_ids={s['id'] for s in selected};views=[v for v in visual if v['source_id'] in source_ids and v['status']=='rendered_observed']
  state_views=[v for v in creative if v['source_id'] in source_ids]
  level='rendered_source_observations' if any(v['status']=='rendered_content_observed' for v in state_views) else 'rendered_geometry' if views else ('http_dom' if selected else 'not_observed')
  goal={'story-index':'选择可用章节，理解阅读顺序并按需恢复已保存的位置。','story':'以明确顺序阅读当前章节，并能切换阅读方式、继续或退出。','prompt':'审阅并编辑分层提示词，理解样例来源并可靠复制原创配方。','careers':'理解雇主理念、工作方式和岗位入口，再审阅符合条件的角色。','gallery':'按主题浏览视觉作品，用可访问的查看器审阅并返回索引。','experiment':'理解输入方式并可控地体验、暂停和退出互动实验。','notfound':'理解资源不可达的原因，并通过有效入口恢复任务。','listing':'帮助用户在完整结果中定位条目，并进入详情或恢复空结果。','directory':'根据实体身份和明确筛选找到合适的对象。','portal':'让用户理解内容层级，并进入当前最重要的任务。','award':'理解作品、奖项与来源，并安全进入原站或相关内容。','pricing':'理解计费周期和权益限制，再审阅明确的方案。','wizard':'分步收集最少必要输入，在最终行动前审阅和确认。','course':'理解课程与大纲，明确公开预览和访问权限。','product':'核对产品、规格、许可与费用，完成可核实的选择。','job':'理解岗位及申请条件，进入明确的申请路径。','contact':'完成可恢复的询问表单并理解提交的实际状态。','faq':'找到相关答案，理解下一步及帮助渠道。','event':'理解活动时间、议程、地点与参与条件。','article':'按章节持续阅读并追溯事实、版本和引用。','profile':'理解身份、贡献、作品与公开联系边界。','project':'理解项目问题、过程、贡献和有证据的成果。','about':'理解主体、团队和可核实的背景。','service':'判断服务与当前问题的适配性，并进入咨询。'}[kind]
  contract={'schema_version':'3.0','id':id,'skill':name,'title':title,'kind':kind,'scope':'Awwwards-linked external inner page; specific award status requires official evidence' if id.startswith('external-') else 'Awwwards main-site page family','source_families':families,'goal':goal,'regions':regions.split('、'),'workflow':workflow,'data_fields':fields,'failure_recovery':recovery,'motion_contract':motion,'evidence_level':level,'source_relationship_note':'An outbound work-detail association does not certify that every current inner page won an award or matches a historical version.','evidence_note':'Only recorded observations are facts. DOM structure does not prove visual composition, hidden state, source code, backend behavior or licenses. The runnable blueprint is an original recipe, not a source-site clone.','sources':[{'id':s['id'],'url':s['url'],'family':s['family'],'inspection_level':s['inspection_level'],'observed_at':s['observed_at'],'source_sha256':s.get('source_sha256'),'structure':s['structure']} for s in selected],'visual_metrics':views,'source_state_observations':state_views,'source_coverage':'observed_examples' if selected else 'needs_source_inspection','original_blueprint':True,'business_mode':'local_preview','states':['default','loading','empty','error','success_preview','disabled','keyboard_focus','reduced_motion','narrow_view'],'acceptance':[goal,recovery,motion,'320、390、768、1440 宽度不出现整页横溢出；必要表格在独立区域滚动。','键盘可进入、操作、关闭对话框并返回触发点；错误不只靠颜色。','本地预览不得暗示真实支付、投稿、消息、账户或预约已生效。'],'limitations':['Source interaction audit is not automatically performed','Source assets are not bundled','Real backend, production and physical-device acceptance are not included']}
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
   for file in ['index.html','style.css','main.mjs','runtime.mjs']:shutil.copy2(source/file,folder/'assets'/file)
  registry.append({'id':id,'skill':name,'title':title,'kind':kind,'runtime_variant':runtime_variant,'source_families':families,'source_coverage':contract['source_coverage'],'source_count':len(selected),'evidence_level':level,'path':folder.relative_to(R).as_posix(),'demo':folder.relative_to(R).as_posix()+'/assets/','browser_validation':'See validation evidence; not inferred from generation'})
 out={'schema_version':'3.0','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'core_skills_preserved':24,'page_skills':len(registry),'status':'in_progress','scope':'Awwwards main pages and awarded external-site inner pages, organized into reusable task-specific skills','not_claimed':['All pages visited','All awarded websites fully analyzed','All source interactions reproduced'],'skills':registry}
 write(R/'page_skills/registry.json',json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'page_skills':len(registry),'observed_page_families':sum(x['source_coverage']=='observed_examples' for x in registry),'requires_source_inspection':sum(x['source_coverage']!='observed_examples' for x in registry)},ensure_ascii=True));return out
if __name__=='__main__':generate()
