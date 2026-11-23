---
name: awwwards-page-external-property-explorer
description: Design and implement real-estate property exploration pages with linked 3D or static space selection, instant filters, catalogue details and recovery.
---

# 获奖来源外站房地产三维浏览、即时筛选与房源比较

## 适用任务
在原创房地产空间研究中比较完整房源，使用三维或静态路径选择、返回并生成本地简报。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `rendered_source_observations`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：项目身份、原创静态图、可选真实三维、视角与时间、完整房源目录、即时筛选、选择与详情返回、本地研究简报、恢复与清理。
1. 先等待实际场景并人工核对，加载进度或画布尺寸不证明正常三维已显示；视觉大写不一定是实际可访问名称。
2. 区分三维镜头、时间光照示意、楼栋房源和筛选抽屉，记录状态作用区域；归一化时间步长不等于小时。
3. 核实筛选是即时还是关闭后应用；完整目录数量、已确认过滤和未完成输入分开，未知面积或状态不变成零或可售。
4. 图形中选择与键盘列表提供等价路径；详情、返回与浏览器历史恢复筛选、视角、焦点和位置，深链不擅自离开页面。
5. 原创图形按需绘制，有轻量档与静态路径；图形加载失败、上下文丢失、数据摘要变化和卸载分别恢复或清理。
6. 只生成明确本地的研究简报；工程模型、校准日照、实时库存、价格、预约与询价必须通过真实数据和授权接口另行验收。

## 数据与状态
字段：catalogue_revision, units[].id, building, floor, bay, area_hundredths_or_null, rooms_half_or_null, availability_or_null, confirmed_filters, draft_validity, view, study_hour, selected_space, local_brief, owned_graphics_resources。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：无效范围保留并标记上次已确认结果；数据失败保留完整原创目录；图形失败不阻断筛选和阅读；模块加载失败允许重新载入，图形上下文可重试；旧简报随选择或状态变化失效。

## 动效与响应式
无自动旋转或背景动画，显式操作更新镜头和光照；减少动态也保持静止，触摸滚动不误选；释放当前实例的几何、材质、监听和渲染器，静态内容仍在。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://belgradearbor.rs/en/3d（http_dom；2026-11-23T09:32:15.098546+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。

## 房地产三维浏览专项
读取 `assets/catalogue.json`、`assets/model.mjs`、`assets/scene.mjs`、`assets/asset-origin.json` 与 `property_contract`。先等待真实渲染并审阅画面，核对可访问名称、镜头状态、时间单位和筛选时机；不要把加载进度、画布大小或大写视觉文字当作完成证明。蓝本用原创程序化建筑和完整虚构房源，三维选择与键盘列表等价；即时有效筛选与未完成输入分开，未知面积/状态/价格不补成零或可售。三维显式启用、按需绘制，有静态路径、资源预算、上下文恢复和清理；不依赖运动展示信息。编辑 JSON 后运行 `python render_static.py`。Three许可保留；源站模型、贴图、字体、标志和截图不分发。工程尺度、校准日照、真实库存与询价需另取真实数据和授权接口验证。
