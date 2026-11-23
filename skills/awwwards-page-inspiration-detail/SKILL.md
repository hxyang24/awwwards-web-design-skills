---
name: awwwards-page-inspiration-detail
description: Design and implement a inspiration detail page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 主站灵感参考详情、媒体说明与本地笔记

## 适用任务
理解媒体参考的身份、出处和边界，明确播放与记录本机观察，并可靠恢复失败。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `rendered_source_observations`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：参考身份、出处与创作者、原创媒体、播放状态、文字稿、静态主题、本地笔记、链接复制、相关参考与返回。
1. 区分参考媒体与源站真实互动，不将视频当作可运行原作
2. 核查媒体时间与错误，而不是仅看海报
3. 确认标签是说明还是入口，匿名收藏是否要求账户
4. 明确播放并可暂停或回到首帧，文字稿始终保留
5. 本机笔记明确保存范围，复制失败提供手工路径

## 数据与状态
字段：reference_id, creator, source_url_or_null, media_file, media_duration, transcript_segments, static_tags, related_notes, notebook_version, local_notes, persistence_scope, clipboard_result。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：媒体失败保留海报与完整文字稿；存储不可用只保留当前标签页并说明旧记录可能存在；编辑后下载失效；复制未确认不报成功。

## 动效与响应式
蓝本没有自动播放；明确点击才播放原创静音短片；支持暂停、定位、重置，减少动态时仍默认静态并保留全文。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://www.awwwards.com/inspiration/20-years-of-xbox-museum-3d-environments-microverse（http_dom；2026-11-23T08:40:27.306104+00:00）
- https://www.awwwards.com/inspiration/20-years-of-xbox-museum-timeline（http_dom；2026-11-23T08:40:27.365576+00:00）
- https://www.awwwards.com/inspiration/2021-virtual-webbys-cta-button-to-enter（http_dom；2026-11-23T08:40:27.424218+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。

## 灵感参考详情专项
读取 `assets/reference.json`、`assets/model.mjs`、`assets/media-origin.json` 和 `reference_contract`。先区分参考影片与原作互动，再核查媒体元数据、实际时间推进、文字说明、出处、标签与匿名收藏边界。蓝本采用独立原创静音短片、明确播放、完整文字稿、本机笔记与手工复制回退；不是原站账户或收藏服务。编辑 JSON 后运行模板内 `python render_static.py`。公开素材均为原创，原站品牌、画面、字体和截图不打包；换入真实参考须核验授权、出处和版本。
