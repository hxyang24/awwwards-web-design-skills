---
name: awwwards-page-external-prompt-detail
description: Design and implement a external prompt detail page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 获奖来源外站提示词与字体效果详情

## 适用任务
审阅并编辑分层提示词，理解样例来源并可靠复制原创配方。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `rendered_source_observations`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：效果身份、文字输入、分层配方、复制与失败恢复、结果对比、解释与服务边界。
1. 把用户文字、字形描述和场景描述分成可检查的层，保留 Unicode 和文本方向，不把图像提示词称作可安装字体。
2. 编辑时更新本地组合文本；复制必须等待剪贴板实际成功，拒绝时提供选中和手动复制。
3. 结果切换使用可访问选项卡或对比视图；模型结果必须来自真实记录，原创 CSS 示意不冒充模型基准。
4. 生成入口与配方编辑分开；接入前确认提供者、费用、发送内容和素材许可，未接入时不宣称生成成功。

## 数据与状态
字段：exact_text, letterform_layer, scene_layer, composed_prompt, direction, clipboard_status, result_provenance, provider_boundary。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：空文字、长度超限和剪贴板拒绝有可恢复提示；任何失败不丢失已编辑配方。

## 动效与响应式
移动端分层内容可折叠并保留完整可选文本；查看器、选项卡和关闭都有键盘路径。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://aifont.ai/fonts/tagging-letters（http_dom；2026-11-23T08:47:44.618386+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。
