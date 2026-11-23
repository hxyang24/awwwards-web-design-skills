---
name: awwwards-page-external-technical-product
description: Design and implement a external technical product page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 获奖来源外站技术产品详情与证据分级

## 适用任务
核对产品身份、示例尺寸与性能证据，选择示意配置并生成本地项目简报。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `rendered_source_observations`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：产品身份、原创示意、规格、性能证据、饰面、配置示意、下载、本地项目简报、常见问题。
1. 辨认详情任务，不按 collection 路径误分为集合页
2. 核实面板切换、预设状态和实际滚动容器
3. 区分示例尺寸、未知性能与带文档输入
4. 用键盘选择面板、饰面和示意布局
5. 生成本地简报并说明未提交任何询价

## 数据与状态
字段：product_identity, example_dimensions_mm, performance[].value_or_null, performance[].basis, performance[].reference, finishes, symbolic_layouts, active_panel, selection_route, local_brief。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：数据失败保留完整静态四节与下载；未知性能不能记为零或认证；编辑后废弃旧简报。

## 动效与响应式
默认静态原创图示，无自动视频；减弱动态时无装饰运动；二维配置示意不冒充工程或三维配置器。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://fluid.glass/collection/fluid-folding-door（http_dom；2026-11-23T14:33:34.453486+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。

## 技术产品详情专项
读取 `assets/model.mjs`、`assets/product.json` 与 `technical_contract`。先核实详情身份和真实内容面板，记录容器滚动与可见内容变化，不把 window.scrollY 不变误判为无交互。蓝本采用四个可访问面板、示例尺寸单位转换、未知性能、原创饰面与二维配置示意，以及仅本地的项目简报。修改数据后运行 `python render_static.py` 更新静态全文和下载文件；完整数据摘要不符时保留静态内容。厂商规格与认证必须另取授权并核验适用版本；当前不含真实询价、三维配置器或源站素材。
