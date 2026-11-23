---
name: awwwards-page-external-story-index
description: Design and implement a external story index page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 获奖来源外站叙事章节索引

## 适用任务
选择可用章节，理解阅读顺序并按需恢复已保存的位置。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `rendered_source_observations`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：故事身份、章节封面、可用状态、阅读入口、保存位置、阅读说明。
1. 将故事、章节、可用状态和阅读进度分别建模；未发布章节不伪造可点击入口。
2. 保留章节的稳定地址与返回索引路径；媒体加载或画布失败不阻断章节标题和文字。
3. 进度仅在明确选择后保存在本机；损坏或不可用的存储不影响阅读。
4. 原创蓝本提供三章、逐格/全文阅读、可选本地记忆和不可用章节恢复；不复制源站角色、画面或音乐。

## 数据与状态
字段：story_id, chapters, availability, reading_progress, storage_consent, media_rights。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：未发布、链接错误和本地存储失败分别说明；任何错误都能返回可用章节。

## 动效与响应式
章节不会自动跳转或强制播放；图形和声音是可拒绝的增强。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://ponpon-mania.com/chapters（http_dom；2026-11-23T08:43:55.031216+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。
