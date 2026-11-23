---
name: awwwards-page-external-about
description: Design and implement a external about page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 获奖外站团队与关于内页

## 适用任务
理解主体、团队和可核实的背景。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `http_dom`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：品牌故事、理念、团队、能力、历史、联系。
1. 从实际内页提取章节及信息层级，区分制作方与客户。
2. 人员、角色、地点和资质按公开资料核验。
3. 保留故事结构但用原创文案和已授权肖像。

## 数据与状态
字段：story, principles, team, capabilities, history, contact。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：缺少照片或介绍时用明确占位；不编造团队成员。

## 动效与响应式
长叙事提供章节入口，手机保留内容顺序和可触达联系。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://aim.obys.agency/about（http_dom；2026-11-23T08:04:09.948300+00:00）
- https://aristidebenoist.com/about（http_dom；2026-11-23T08:04:41.196079+00:00）
- https://bennettandclive.com/about/（http_dom；2026-11-23T08:05:03.673013+00:00）
- https://carterogunsola.com/about（http_dom；2026-11-23T08:05:51.201638+00:00）
- https://carterogunsola.com/studio（http_dom；2026-11-23T08:05:51.206533+00:00）
- https://www.197historiasilustradas.com/en/about-us（http_dom；2026-11-23T08:03:08.628736+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。
