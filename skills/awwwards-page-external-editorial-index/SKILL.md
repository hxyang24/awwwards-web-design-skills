---
name: awwwards-page-external-editorial-index
description: Design and implement a external editorial index page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 获奖来源外站杂志与文章索引

## 适用任务
按主题和完整目录搜索发现文章，并可靠继续加载、阅读与返回。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `rendered_source_observations`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：期刊身份、精选故事、主题导航、全文搜索与排序、文章卡片、渐进加载、阅读入口、完整静态内容与恢复。
1. 把精选故事与可筛选目录分开；文章身份、主题、日期和作者使用独立字段，日期未知时不补造。
2. 明确搜索覆盖完整目录还是仅已加载条目；主题、查询、排序和已展开位置可在地址及返回路径中恢复。
3. 加载更多只追加新记录，保留原有条目与焦点；失败后保留已读列表并允许对同一游标重试。
4. 取消或忽略过期请求，防止旧筛选结果覆盖新筛选；无结果、加载失败和无效主题分别解释。
5. 阅读入口有可访问的完整原文路径，返回索引恢复主题、已展开条目和触发点；无脚本或资源失败时保留完整原创示例。

## 数据与状态
字段：catalog_version, featured_article, topics, articles[].id, title, summary, author, published_at_or_null, query, sort, cursor, confirmed_total, loaded_count, reading_origin。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：目录请求失败不能冒充零文章；加载更多失败保留已展示条目与旧游标；无效阅读地址可返回有效目录。

## 动效与响应式
不依赖动效传达更新；新增条目不整页重排，键盘可跳转到新条目；移动端主题换行且控件不遮挡阅读。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://apinistudio.com/blogs/notizie（http_dom；2026-11-23T09:09:35.407734+00:00）
- https://www.emilynixon.com/blogs/b-66/（http_dom；2026-11-23T10:52:34.336987+00:00）
- http://aonnoysengupta.com/blog（http_dom；2026-11-23T09:10:15.179750+00:00）
- http://www.blacknegative.com/news/（http_dom；2026-11-23T08:15:57.604064+00:00）
- https://abelfragrance.com/blogs/journal（http_dom；2026-11-23T12:24:22.048279+00:00）
- https://abelfragrance.com/blogs/journal?page=2（http_dom；2026-11-23T12:35:57.751066+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。

## 杂志索引专项
读取 `assets/catalog.mjs`、`assets/articles.json` 和契约中的 `editorial_contract`。示例使用独立原创全文和本地异步分页适配器，不复刻源站后端。编辑数据后重新生成完整静态正文；移植到真实服务时保留服务端完整查询、游标版本、已确认数量和失败状态。来源只观察了有限主题与加载动作，不代表所有文章已审阅。
