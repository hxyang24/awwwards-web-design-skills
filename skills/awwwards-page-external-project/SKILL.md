---
name: awwwards-page-external-project
description: Design and implement a external project page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 获奖外站项目与案例内页

## 适用任务
理解项目问题、过程、贡献和有证据的成果。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `rendered_geometry`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：项目身份、问题、角色、过程、成果、媒体、证据、下一项目。
1. 将委托方目标、制作方贡献和实际成果分开。
2. 项目媒体记录所有者与许可，不能因公开展示就打包复制。
3. 使用语义章节重建叙事，再补媒体和转场；下一项目可直接链接。

## 数据与状态
字段：project, client, roles, problem, process, outcome, evidence, media_rights。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：案例数据不足时保留未知；媒体失败不阻止阅读与导航。

## 动效与响应式
固定章节与图像过渡要保持正文可读；减少动画直接展示。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://alitwotimes.com/work/amazon-the-biggest-sale-of-the-year/（http_dom；2026-11-23T08:18:00.072945+00:00）
- https://alitwotimes.com/work/badya-life-imitates-art/（http_dom；2026-11-23T08:18:00.113808+00:00）
- https://alitwotimes.com/work/bud-light-millennial-beach/（http_dom；2026-11-23T08:18:00.224693+00:00）
- https://alitwotimes.com/work/changing-diner/（http_dom；2026-11-23T08:19:30.257588+00:00）
- https://alitwotimes.com/work/cheers-to-all-fans/（http_dom；2026-11-23T08:20:03.962961+00:00）
- https://alitwotimes.com/work/du-tuesday-the-man-sitting-next-to-you/（http_dom；2026-11-23T08:20:03.998549+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。
