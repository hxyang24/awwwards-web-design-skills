---
name: awwwards-page-external-product
description: Design and implement a external product page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 获奖外站产品与商店内页

## 适用任务
核对产品、规格、许可与费用，完成可核实的选择。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `rendered_source_observations`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：产品身份、展示、规格或变体、库存、许可、价格、购买条件。
1. 先识别实体商品、数字产品或服务，再选择数据和状态模型。
2. 规格、变体、库存、税费和配送不从截图推断，缺少接口时明确。
3. 选择、审阅与付款是独立状态，原站素材需许可。

## 数据与状态
字段：product, type, variants, stock, price, currency, terms, licensed_media。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：缺货、价格改变和支付失败均可恢复；不可伪造购买。

## 动效与响应式
3D 预览是增强，规格与购买条件保留在 DOM。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

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
- https://marryandbride.com/come-fly-with-me-braut-cape/（http_dom；2026-11-23T12:28:50.024570+00:00）
- http://www.delvaux.com/en/products/accessories/brillant-charms-box-calf-black-dore（http_dom；2026-11-23T10:39:57.242692+00:00）
- https://aoiofficial.com/us/collections/1-of-1（http_dom；2026-11-23T08:49:12.864912+00:00）
- https://aoiofficial.com/us/collections/all（http_dom；2026-11-23T08:49:12.957777+00:00）
- https://aoiofficial.com/us/collections/cashmere（http_dom；2026-11-23T08:49:13.049441+00:00）
- https://becore.se/pages/shop（http_dom；2026-11-23T09:29:40.622673+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。

## 商品详情专项
读取 `assets/product-model.mjs`、`assets/product.json` 和契约中的 `product_contract`。先区分详情与集合页，再核查图库、变体、加急选项、库存和说明折叠。源站透明原生控件可能有可见标签；实际点击已核查标签，不用强制修改隐藏 select 代替用户路径。当前来源只有一种颜色，加急勾选和准备时间的变化已观察；未证明颜色切换或源站价格重算。蓝本为独立原创虚构灯具，保留未知费用、失效估算、售罄和失败恢复；不包含真实购物接口。
