---
name: awwwards-page-course-detail
description: Design and implement a course detail page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 课程详情与大纲

## 适用任务
理解课程与大纲，明确公开预览和访问权限。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `http_dom`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：课程介绍、讲师、预览、大纲、先修条件、访问与价格、评价。
1. 按课程目标列出章节和先修条件，不仅展示营销大图。
2. 区分可公开预览的课时和受购买或登录约束的课时。
3. 切换章节保留播放位置的约定，停止时清理媒体。

## 数据与状态
字段：course, instructor, syllabus[].lessons, preview_access, purchase_state。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：媒体加载失败提供文字说明；受限课时不尝试绕过门槛。

## 动效与响应式
大纲使用可访问展开控件，预览不自动有声播放。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://www.awwwards.com/academy/course/advanced-prototyping-from-early-ideas-to-rich-interactions（http_dom；2026-11-23T08:06:17.195398+00:00）
- https://www.awwwards.com/academy/course/boost-your-conversion-rates-learn-landing-page-design-with-figma（http_dom；2026-11-23T08:06:22.681027+00:00）
- https://www.awwwards.com/academy/course/building-an-immersive-creative-website-from-scratch-without-frameworks（http_dom；2026-11-23T08:06:22.683519+00:00）
- https://www.awwwards.com/academy/course/creating-epic-e-commerce-experiences-for-brands-an-advanced-guide（http_dom；2026-11-23T08:06:22.685895+00:00）
- https://www.awwwards.com/academy/course/creative-coding-2-0-in-js-animation-sound-color（http_dom；2026-11-23T08:06:27.967876+00:00）
- https://www.awwwards.com/academy/course/creative-portfolios-a-powerful-visual-language-for-brands-online-course（http_dom；2026-11-23T08:06:27.970567+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。
