# 商品详情 Skill · 图库、可见选项与可靠估算

本轮完善现有 `awwwards-page-external-product`，技能总数保持 74，不把每个来源网址重复计为一套技能。保留原有 12 套 V1 与 24 套核心技能。

## 来源与实际操作

[marry&bride 商品内页](https://marryandbride.com/come-fly-with-me-braut-cape/) 在 390 和 1440 宽度有浏览器实际观察。[官方作品详情](https://www.awwwards.com/sites/marry-bride) 本轮读取确认该作品获 2026 年 8 月 5 日 Honorable Mention。当前商品内页不因此被宣称独立获奖或与获奖时的版本完全相同。

- 已操作图片第二页、材质护理及配送退换说明；记录到图片选中项和说明状态变化。
- 颜色只有一个可用选项，操作已核查的可见标签后仍为选中。没有另一个颜色，不能声称已验证颜色切换。
- 两种宽度均通过可见标签开启及关闭加急选项，勾选状态与显示的准备时间相应变化，取消后恢复。
- 初始探测只筛选可见原生字段，漏掉隐藏的颜色 select 和透明的加急 checkbox。修正后同时记录可见关联标签及颜色 radio。字段空数组不能用来证明页面没有配置能力。
- 源站价格重算未采集到；没有操作购物车、愿望单、付款、联系消息或任何表单提交。来源浏览器只放行匿名 GET/HEAD，非读取请求被阻止，不能据此推断真实后端行为。

另一 [Cartier 页面](https://www.cartier.com/en-us/loveconfigurator.html) 在手机与宽屏观察均返回 HTTP 403，仍保留缺口。文件名或另一 Cartier 获奖项目不能证明这个页面具备正常可用的配置器或 3D 交互。

来源摘要见 [product-page-observations.json](research/live_pages/product-page-observations.json)。源站完整 HTML、照片与截图不随包分发；只发布来源、有限状态摘要和私有截图哈希。原站价格、服务条款、品牌、字体与媒体没有复制进蓝本。

## 可调用规则与原创模板

读取 [SKILL.md](skills/awwwards-page-external-product/SKILL.md) 与页面契约后，可将规则移植到已有项目，或独立导出 Form Objects 原创灯具详情模板：

```text
python skills/awwwards-page-external-product/scripts/scaffold.py --output YOUR_EMPTY_DIRECTORY
```

进入导出目录启动 `python -m http.server 8000 --bind 127.0.0.1`，打开 http://127.0.0.1:8000/ 。无需 npm 或第三方素材。非空目录拒绝覆盖。

模板包含三种原创 CSS 灯具视图、放大对话框、方向键与焦点返回；原生颜色 radio、尺寸选择、数量和加急选项；已知库存、未知库存、售罄、库存不足的不同恢复路径；材质、配送和估算说明折叠。没有自动轮播。

金额以整数分计算。示例只汇总已知商品金额与按次加急费用；税费、配送和最终应付金额保持 null。编辑后旧估算立即失效并取消请求；新的估算通过后才能审阅。失败可重试并保留选择，旧响应不能覆盖新结果。保存只产生当前页面内的反馈。

无脚本或产品数据失败时，三种原创视图、规格、价格示例与说明仍可读取；选择控件不可用，数据失败有重试。卸载时取消本模块工作、恢复静态内容，并保留宿主页面其他操作。

## 研究工具的边界

`tools/source_fields.mjs` 同时记录原生字段可见性、禁用状态和可见关联标签，不采集字段输入值。可见标签仍不等于无遮挡、唯一、可用或已操作；操作前继续使用唯一目标核查。

`tools/reviewed_family.py` 允许将没有常见路径前缀的确切网址归入已人工核查的任务族，同时保留原启发式分类与证据。复核只绑定当前缓存来源哈希；来源改变或不可用后恢复待复核。分类不会自动标记整页设计提炼完成，也不会扩张到同站其他任意网址。

## 验证与未测

实测回执位于 [商品模型检查](research/product_skill_validation/model-results.json)、[商品浏览器检查](research/product_skill_validation/browser-results.json) 和 [源站字段夹具](research/source_state_validation/field-results.json)。首轮发现尺寸 label 混入全部选项文字，现已改为独立明确标签；禁用检查也改为验证真实选择控件。首轮失败回执保留为 `browser-first-run.json`。

自动化无障碍规则只是局部检查。真机、Safari/Firefox、完整读屏、真实库存与报价接口、购物车、支付、配送、适用法律条款、原站全部隐藏状态及逐像素重建均未验收。全站及所有获奖外站内页仍在持续整理。
