#!/usr/bin/env python3
"""Build distinct source-informed interaction patterns, not generic page aliases."""
from pathlib import Path
import hashlib,json,shutil,datetime
R=Path(__file__).resolve().parents[1]
PATTERNS=[
 {'id':'discovery-navigation','title':'发现门户：巨型标题、分组导航与浮动章节入口','kind':'navigation','page_skills':['awwwards-page-discovery-home','awwwards-page-website-explorer'],'source_ids':['awwwards-explore-wide','awwwards-search-phone'],
  'observed':['主站在 1440 宽度呈现约 127px 的居中主标题，390 宽度约 42px；这是两个具体视口的实测值。','实际点击 Explore 后，可见链接计数由 118 变为 125。源控件是带点击行为的 span，不据此声称其键盘或 ARIA 已合格。','页面存在搜索表单；本轮只读策略排除了提交按钮，因此未执行原站搜索。'],
  'recipe':['将跨页面导航、站内章节入口和搜索分成三种独立状态，避免一个按钮承担多重含义。','用 button、aria-expanded 和关联 nav 实现分组导航；打开后可进入链接，Escape、离开区域或点击外部可关闭并维护焦点。','主标题按内容压力缩放，底部章节导航与提示层预留空间，不遮挡主要操作。','本地搜索只是原创蓝本的结果筛选，接真实接口时重新定义查询、加载、空结果和失败恢复。'],
  'invariants':['主导航、章节跳转与搜索结果均可用键盘访问。','导航缩窄后不得让焦点留在隐藏区域；提示层不能挡住底部入口。','源站字体仅作为测量事实，不打包其字体文件或品牌资产。','按钮点击后必须检查展开、焦点或结果的实际变化，不仅检查按钮存在。'],
  'limits':['原站搜索未提交；蓝本搜索不是原站搜索的复刻。','版式配方使用原创几何和系统字体，不声称逐像素一致。']},
 {'id':'careers-culture','title':'招聘品牌页：双层导航、可控视觉与价值观画廊','kind':'careers','page_skills':['awwwards-page-external-careers','awwwards-page-job-board'],'source_ids':['apple-careers-wide','apple-careers-phone'],
  'observed':['招聘页在 1440/390 宽度的主标题约为 75/38px，均为白字深色背景；这是当前页面的视口观察，不是所有招聘页的规范。','桌面主动请求动画后，控制标签发生变化；本轮没有播放人物影片，也未验证媒体后端。','手机局部导航与全站导航分别操作后，可见链接数量发生变化；价值观画廊的下一项操作也观察到状态变化。'],
  'recipe':['将品牌层、招聘局部导航、团队价值和岗位浏览分区；手机局部导航可独立展开，不能淹没岗位入口。','所有动效初始可静止；用户主动播放后提供暂停，离屏、隐藏标签和偏好改变时停帧。','画廊展示单一活动项，提供前后按钮、箭头键、当前位置和减少动画路径，不强制自动轮播。','岗位数据与品牌叙事分开；本地虚构岗位支持查询、团队过滤、空结果恢复和详情审阅，真实申请系统单独接入。'],
  'invariants':['局部导航和全站导航不是同一状态；移动折叠后焦点仍可用。','不复制原站商标、音乐、影片、插图或真实岗位文案。','画廊隐藏项不能包含仍可聚焦的控制。','没有 ATS、邮件或数据库时，不显示真实申请成功；不得采集简历或敏感资料。'],
  'limits':['观察到的控制变化不代表影片播放、申请提交或全部岗位流程已测。','来源位于获奖来源站点的当前内页，不声称该招聘页单独获得奖项或与历史获奖版本相同。']},
 {'id':'immersive-fallback','title':'沉浸式站点：图形增强失败时仍保留可用页面','kind':'immersive','page_skills':['awwwards-page-external-home','awwwards-page-external-experiment','awwwards-3d-experience'],'source_ids':['active-theory-compatibility-fallback'],
  'observed':['本轮匿名软件图形环境的实际截图出现了浏览器不支持的提示和静态视觉。','这是特定环境下的兼容回退观察，未验证该站正常图形体验，也不据此评价所有用户的浏览结果。'],
  'recipe':['先以 DOM 交付项目、导航、说明和联系路径，图形层不得拥有唯一任务入口。','增强层有初始化、静止、运动、暂停、回退和销毁状态；WebGL 初始化或 context loss 失败时可读内容保持可用。','为当前增强实例记录资源所有权；卸载移除观察器、事件、动画帧并释放几何、材质与渲染器。','限制 DPR、粒子和几何预算，提供轻量档；离屏和隐藏标签停帧，减少动画时仅绘制稳定视图。'],
  'invariants':['禁用 JavaScript、图形不可用或手动选择静态时，核心链接和项目文本仍在页面。','兼容失败不等于正常源站体验完成；原站技术版本与内部 shader 不得从图像猜测。','资源清理只释放当前实例所有的资源，不全局销毁其他页面。','原创建模与有许可的 Three.js 分开标记；保留 MIT 文本。'],
  'limits':['本轮源站正常三维交互未观察，示例为原创替代实现。','软件 WebGL 验证不能替代真实 GPU、手机和生产验收。']}
]
PATTERNS.append({
 'id':'bounded-physics','title':'有界物理装饰：可控对象、等价输入与静态替代','kind':'physics',
 'page_skills':['awwwards-page-external-about','awwwards-page-external-experiment','awwwards-advanced-motion'],
 'source_ids':['ponpon-about-physics-phone','ponpon-about-physics-wide'],
 'observed':['官方作品页将 About 物理效果列为展示点；本轮 About 的两种宽度都显示画布中的装饰性对象堆叠。','修正采样工具多余 Escape 输入后，页面保持 About；指针采样期间对象位置发生重排。','抓取跟随、精确受力、碰撞规则和源站引擎版本尚未确认；不能把像素变化单独算作对应手势已验证。'],
 'recipe':['将物理效果作为说明、导航与内容之外的增强层，保留静态内容及可退出路径。','为对象数量、世界边界、速度与单帧追赶设预算；使用固定时间步，隐藏或离屏后不积累巨大补偿。','指针直接操作同时提供对象选择、按钮与键盘等价操作；指针取消或丢失捕获时解除约束。','播放由用户请求，提供暂停、重置、减少动画和静态路径；销毁取消动画帧、释放对象并移除观察器与事件。'],
 'invariants':['示例中的圆、文字和动力学代码为原创，不复制源站角色、音乐或引擎。','对象保持边界内且参数有界；模拟是装饰用途，不是科学或生产物理求解器。','减少动画时不自动积分；手动定位仍可用，离屏返回不会自行播放。','任何输入失败、图形不可用或卸载都不应锁住页面滚动、导航或已有内容。'],
 'limits':['源站对象抓取和移动端真实触控尚未确认；原创示例的拖动不是源站手感复刻。','软件浏览器测试不等于真机、完整辅助技术或生产性能验收。']})

def write(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8',newline='\n')
def asset_digest(folder):
 h=hashlib.sha256()
 for p in sorted(folder.rglob('*')):
  if p.is_file():
   p.stat();h.update(p.relative_to(folder).as_posix().encode())
   with p.open('rb') as f:
    while block:=f.read(262144):h.update(block)
 return h.hexdigest()
def build():
 observations=json.loads((R/'research/live_pages/interaction-observations.json').read_text(encoding='utf-8'))['observations'];byid={x['id']:x for x in observations};registry=[]
 for row in PATTERNS:
  name='awwwards-pattern-'+row['id'];folder=R/'skills'/name;source=R/'interaction_skills/assets'/row['kind'];dest=folder/'assets';shutil.copytree(source,dest,dirs_exist_ok=True)
  if row['kind']=='immersive':
   vendor=dest/'vendor';vendor.mkdir(exist_ok=True)
   for file in ['three.module.js','three.core.js']:shutil.copy2(R/'package/v2/vendor/three'/file,vendor/file)
   shutil.copy2(R/'package/v2/vendor/three/LICENSE',vendor/'LICENSE')
  evidence=[byid[id] for id in row['source_ids']];contract={**row,'skill':name,'source_evidence':evidence,'source_screenshots_redistributed':False,'implementation':'original runnable pattern','business_mode':'local_fictional_preview','source_reproduction_claim':False,'validation_scope':'Actual fixture tests are recorded separately; source observations do not attest implementation tests'}
  write(folder/'references/pattern-contract.json',json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
  steps='\n'.join(str(i+1)+'. '+step for i,step in enumerate(row['recipe']))
  text=f'''---
name: {name}
description: Implement a distinct {row['id'].replace('-', ' ')} pattern with recorded source-state observations, a standalone original example and explicit fallback, keyboard and lifecycle contracts.
---

# {row['title']}

## 用于什么任务
为相应页面增加此机制。它可以与 {', '.join(row['page_skills'])} 配合；不要因此替换用户既有框架、品牌、接口或其他页面。

## 读取来源与限制
先读 [具体观察与配方](references/pattern-contract.json)。observed 是已记录的来源观察；recipe 是本库的原创实现方法；源站事实、推断和蓝本验证不得混用。

'''+ '\n'.join('- '+x for x in row['observed'])+f'''

## 实施
{steps}

## 不变量与验收
'''+ '\n'.join('- '+x for x in row['invariants'])+'''
- 在 320/390/768/1440 宽度检查阅读顺序、主操作、溢出和焦点；实际操作主路径、失败恢复和减少动画路径。
- passed 需要本次运行证据；未执行的源站状态、真实设备或后端接入保留 not_run/blocked。

## 独立原创蓝本
```text
python scripts/scaffold.py --output YOUR_EMPTY_DIRECTORY
```
在导出目录运行 `python -m http.server 8000 --bind 127.0.0.1` 并访问 http://127.0.0.1:8000/ 。拒绝覆盖非空目录，不依赖 npm 或原站素材。Three.js 示例保留其 MIT 文件。

## 剩余边界
'''+ '\n'.join('- '+x for x in row['limits'])+'\n\n原站图像、字体、视频、音乐和标志不随技能分发。所有示例文案、几何和行为代码为原创；第三方库适用各自许可。\n'
  if row['kind']!='immersive':text=text.replace('Three.js 示例保留其 MIT 文件。','此示例不加载原站代码或第三方运行库。')
  write(folder/'SKILL.md',text)
  write(folder/'scripts/scaffold.py','''#!/usr/bin/env python3
from pathlib import Path
import argparse,shutil,json
SOURCE=Path(__file__).resolve().parents[1]/'assets'
def scaffold(output):
 target=Path(output).expanduser().resolve()
 if target==SOURCE or SOURCE in target.parents:raise ValueError('Choose a directory outside the source assets')
 if target.exists() and any(target.iterdir()):raise ValueError('Refusing to overwrite a nonempty directory')
 target.mkdir(parents=True,exist_ok=True)
 for p in SOURCE.iterdir():
  if p.is_dir():shutil.copytree(p,target/p.name)
  else:shutil.copy2(p,target/p.name)
 return {'mode':'original_local_pattern','output':str(target),'start':'python -m http.server 8000 --bind 127.0.0.1'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
 try:print(json.dumps(scaffold(a.output)))
 except (ValueError,OSError) as e:p.exit(2,str(e)+'\\n')
''')
  registry.append({'id':row['id'],'skill':name,'title':row['title'],'kind':row['kind'],'path':folder.relative_to(R).as_posix(),'demo':folder.relative_to(R).as_posix()+'/assets/','supports_page_skills':row['page_skills'],'source_observation_ids':row['source_ids'],'asset_sha256':asset_digest(dest),'source_normal_experience_validated':False,'status':'original_pattern_with_limited_source_observations'})
 output={'schema_version':'1.0','recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'in_progress','interaction_skills':len(registry),'scope':'Specific source-informed mechanisms complement page-level skills; not exhaustive site coverage','skills':registry}
 write(R/'interaction_skills/registry.json',json.dumps(output,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'interaction_skills':len(registry),'source_observations_used':len(byid)}));return output
if __name__=='__main__':build()
