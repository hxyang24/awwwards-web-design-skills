---
name: awwwards-page-editorial-article
description: Design and implement a editorial article page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 文章详情与技术拆解

## 适用任务
按章节持续阅读并追溯事实、版本和引用。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `rendered_geometry`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：标题、作者与日期、目录、正文、示例、引用、相关内容。
1. 把公开事实、制作方说明、分析推断和原创实现分段标明。
2. 技术版本以带日期的可靠来源为准。
3. 代码片段和素材保留许可，不把可见图片自动写入项目。

## 数据与状态
字段：article, author, published_at, updated_at, sections, references, rights。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：外链失效保留原引用和访问时间；不补造技术事实。

## 动效与响应式
目录与阅读进度不接管滚动，媒体可暂停，正文始终可读。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://www.awwwards.com/30-great-websites-with-parallax-scrolling.html（http_dom；2026-11-23T08:06:12.968665+00:00）
- https://www.awwwards.com/a-studio-between-two-worlds.html（http_dom；2026-11-23T08:06:17.192619+00:00）
- https://www.awwwards.com/awwards-interview-bonhomme.html（http_dom；2026-11-23T08:07:11.927199+00:00）
- https://www.awwwards.com/best-free-fonts.html（http_dom；2026-11-23T08:07:54.326751+00:00）
- https://www.awwwards.com/breaking-walls-of-conservatism.html（http_dom；2026-11-23T08:08:01.320170+00:00）
- https://www.awwwards.com/capitolium-a-digital-hub-for-a-first-of-its-kind-sports-collaboration.html（http_dom；2026-11-23T08:08:01.325591+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。
