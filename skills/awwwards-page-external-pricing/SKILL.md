---
name: awwwards-page-external-pricing
description: Design and implement a external pricing page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 获奖来源外站定价、套餐比较与用量估算

## 适用任务
理解计费周期和权益限制，再审阅明确的方案。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `rendered_source_observations`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：计费口径、套餐与月费、权益比较、计算单位、用量输入、估算明细、假设与恢复、审阅。
1. 把月费、资源费率和实际工作量的单位分别建模；切换单价展示不能改变工作量或最终估算。
2. 对请求数、运行时长、硬件及分配量给出明确精度和边界；小数、空值、负数或超限不能静默改写。
3. 逐项计算并公开舍入口径和未计成本；未知自定义月费时保留未知总价，已知用量可以单独显示。
4. 手机比较选项卡独立于估算套餐选择，提供键盘、宽屏表格和无脚本的全部内容。
5. 审阅显示当前有效估算及假设；本地蓝本不创建真实账户、报价、购买或订单。

## 数据与状态
字段：tariff_version, currency, workspace_plan, base_fee, rate_unit, requests_per_month, active_seconds, hardware, resource_counts, storage, rounding, known_usage, unknown_costs。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：输入变化后旧估算不可冒充当前值；错误定位至相应字段并可恢复；源数据失败保留静态示例、全部套餐与单位说明。

## 动效与响应式
不依赖动效解释价格变化；单位切换只更新可读数值与说明，移动比较切换和断点重排保持焦点。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://cerebrium.ai/pricing（http_dom；2026-11-23T09:45:42.896551+00:00）
- https://happenboard.com/pricing/（http_dom；2026-11-23T11:23:57.769456+00:00）
- https://humanz.net.au/pricing（http_dom；2026-11-23T11:39:50.261015+00:00）
- https://instinctor.com/pricing/（http_dom；2026-11-23T11:46:26.464673+00:00）
- https://lagrowthmachine.com/pricing/（http_dom；2026-11-23T11:58:26.180478+00:00）
- https://reapi.ai/blog/category/pricing（http_dom；2026-11-23T11:20:42.759048+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。

## 定价专项实施
读取 `assets/pricing-model.mjs` 和契约中的 `estimate_contract`。它们是独立原创虚构费率模型，不是源站计费实现。以整数金额汇总和舍入，明确单位、输入精度、未知费用和旧估算失效。源站小数输入的具体观察不能被当成建议规则。按这些边界操作所有核心路径，再接真实服务端费率和购买接口。
