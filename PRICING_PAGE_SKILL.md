# 定价、套餐比较与用量估算页面 Skill

`awwwards-page-external-pricing` 提炼获奖关联外站的定价内页任务，交付独立原创 Field / Compute 蓝本。它将套餐月费、按量费率、输入精度、估算明细、比较状态与未知费用分别建模，可移植至现有项目的框架与真实计费接口。

## 实际来源与观察边界

[Cerebrium 的 Awwwards 详情](https://www.awwwards.com/sites/cerebrium) 在本次读取中报告 SOTD，并列出定价计算器为展示内容。[当前定价内页](https://cerebrium.ai/pricing) 的 390/1440 宽度均有匿名只读状态记录。源站截图留在私有研究缓存，仅分发摘要和校验哈希。

实际操作了每秒/每小时选项卡、运行时长增量控件、用量输入和 FAQ；手机套餐比较选项卡也有操作记录。时长由 2 变为 3，估算文字随之变化；本次输入 2.5 后源站显示 25，属于观察到的解析行为，不作为建议实现。宽屏区域显示输入与估算面板并列；手机版本在当前区域主要显示输入，不能据此宣称全部手机状态完成。

这不证明源站计费后端、所有硬件选项、费率精度或服务承诺已验证。官方奖项关联也不表示当前内页单独获奖或保持历史版本。其他 HTTP 来源是同类页面候选，不冒充逐一视觉验收。

## Skill 的实施规则

- 区分套餐月费、计算资源的费率显示单位和工作量单位。切换每秒/每小时只改变单价展示，运行时长仍以秒输入，估算总价不变。
- 对请求数、时长、资源数量和存储给出明确界限。接受的精度必须保持原意；无效小数、空值、负数、科学记数或超限输入显示错误并可修正。
- 用整数精度计算，先汇总每项月度成本再舍入。公开费率版本、币种、舍入口径、免费存储和未计成本。不要以界面中的已舍入单价反推账单。
- 未知自定义月费保留未知总价；单独显示可计算的用量。零计算量仍可能存在月费和存储成本。
- 手机比较采用键盘可操作的选项卡，宽屏提供完整表格；切换比较对象不改变估算所选套餐。跨断点变化恢复焦点。
- 编辑后旧估算立即失效，重新计算后才能审阅；无脚本或契约失败时保留全部套餐、费率与完整静态示例。

这些是原创配方与示范实现，源站观察和建议规则分别写入契约。真实计费需用服务端可信费率、权限及最终账单重新验收。

## 原创蓝本与运行

Field / Compute 使用虚构 Seed、Studio、Custom 套餐以及 Aster/Orion 硬件。价格、文案、版式和模型均为原创示范；不复制源站费率表、品牌、字体、图形或代码。模型以 BigInt 计算整数金额，默认例子的月度总额为 $30.05；不是实际可购买服务。

```text
python tools/install_all_skills.py --target YOUR_SKILLS_DIRECTORY
python skills/awwwards-page-external-pricing/scripts/scaffold.py --output YOUR_EMPTY_DIRECTORY
```

在导出目录运行 `python -m http.server 8000 --bind 127.0.0.1`，打开 http://127.0.0.1:8000/ 。无需 npm 或第三方素材。源包中模型为 `page_skills/business/pricing/pricing-model.mjs`，生成的 Skill 自带同一实现。

## 实测与未测

模型 10 项检查通过，覆盖独立算例、单位维度、显示换算、小数精度、超出浮点安全乘积的大用量、零计算量、CPU 路径、未知月费、半分舍入和无效标识。

23 组浏览器专项通过，覆盖四种宽度、两次选定无障碍扫描、输入错误、估算失效、套餐与比较独立性、断点焦点、重置、审阅、无脚本和契约失败。首轮发现重置控件名称遮蔽了浏览器表单方法，已更名修复；保留首轮失败回执，最终状态以 [专项回执](research/pricing_skill_validation/browser-results.json) 为准。

[模型回执](research/pricing_skill_validation/model-results.json) · [来源摘要](research/live_pages/pricing-page-observations.json) · [页面契约](skills/awwwards-page-external-pricing/references/page-contract.json)。

未测真实报价、支付或账单；未验收全部源站状态、真机、Safari/Firefox 及完整辅助技术。没有接入账户或购买流程。自动规则扫描不能替代完整无障碍验收。页面保留生命周期的检查使用受控信号，不代表所有浏览器缓存恢复均已验收。

全站提炼仍在进行。查看 [完整范围与待办](docs/FULL_SITE_SKILLS_GOAL.md)，不能以新增这一页代表全部定价网站或全部获奖内页已经完成。
