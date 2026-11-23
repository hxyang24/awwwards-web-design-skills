---
name: awwwards-page-external-collection
description: Design and implement a external collection page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 获奖来源外站商店、商品集合与即时筛选

## 适用任务
按明确的即时筛选与完整目录查询发现商品，并可靠继续浏览、查看信息和返回。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `rendered_source_observations`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：集合身份、完整目录搜索、排序、即时筛选抽屉、当前筛选、结果与数量、渐进加载、商品信息与返回、完整静态目录。
1. 把商品集合与单个商品详情区分；稳定商品身份、分类、价格未知值和可用状态分别建模。
2. 先实际观察筛选是即时查询还是明确应用，再制定地址、数量、关闭与返回规则；关闭即时筛选抽屉不会撤销已确认选择。
3. 完整目录查询与当前已加载条目分开；分类内多选采用 OR，不同维度采用 AND，并说明各选项数量的计算口径。
4. 失败保留已确认结果、已加载位置和重试入口；请求中的选择、已确认结果和未知数量不能混成同一状态。
5. 商品信息入口有完整文字与稳定地址；返回恢复筛选、排序、展开位置和触发焦点，数据编辑后重新生成无脚本内容。

## 数据与状态
字段：catalog_revision, products[].id, category, price_cents_or_null, availability, query, sort, selected_facets, facet_counts, confirmed_total, cursor, shown_count, reading_origin。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：查询失败不表示零结果；旧请求不得覆盖新选择，加载更多失败保留卡片与游标；无脚本和数据失败可读取全部原创商品信息。

## 动效与响应式
筛选结果依靠可读数量和状态传达；抽屉可键盘关闭并恢复焦点，移动重排不遮挡核心控件。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://marryandbride.com/shop/（http_dom；2026-11-23T12:28:50.349620+00:00）
- http://www.delvaux.com/en/collections（http_dom；2026-11-23T10:39:56.699707+00:00）
- https://acmecups.nz/collections（http_dom；2026-11-23T08:47:53.086202+00:00）
- https://acmecups.nz/collections?page=2（http_dom；2026-11-23T09:34:05.987624+00:00）
- https://acmecups.nz/collections?page=3（http_dom；2026-11-23T09:34:06.160014+00:00）
- https://adinabuzatu.ro/collection/abc（http_dom；2026-11-23T08:47:18.578544+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。

## 商品集合专项
读取 `assets/catalog.mjs`、`assets/catalog.json` 及 `collection_contract`。蓝本采用即时查询：更改选项即更新结果，关闭抽屉保留已确认过滤。它是独立原创虚构目录，不复刻源站数据或后端。移植真实服务时保持已确认数量、未知价格、游标版本、失败恢复及列表返回。编辑 JSON 后运行模板内 `python render_static.py` 更新完整静态目录，再测试所有主路径。源站报告数量和单次查询响应不等于全部库存或所有组合已验收。
