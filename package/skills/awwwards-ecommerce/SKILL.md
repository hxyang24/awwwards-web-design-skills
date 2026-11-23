---
name: awwwards-ecommerce
description: Build product, cart, checkout and after-sales interfaces with inventory limits, integer totals and honest payment state.
---

# 电商完整路径

从商品变体与库存开始，再实现购物车、审阅和结算。价格和库存最终由服务端重算；浏览器总价不可信。

## 输入与边界
读取用户目标、已有项目、允许修改的范围、目标设备和可用业务接口。缺省使用明确标识的本地样例；不要要求与当前任务无关的部署、审批或配置。

## 执行
1. 定义 SKU、变体、库存、货币、税费和配送规则。
2. 加购和改量校验库存；购物车空态和缺货可恢复。
3. 结算提交前展示所有费用，保留错误后的输入。
4. 支付使用合规服务商令牌；只接受服务端验证的回调作为支付事实。
5. 订单、物流、取消和退款分别建模；重复请求用幂等键。

## 交付与检查
输出 checkout-contract、pricing-examples、order/return 状态图与支付边界。Forma 的本地订单不是付款凭证。

根据任务读取 [专项执行契约](references/contract.md)。如与原有 V1 技能共同使用，保留已有脚本和接口；V2 负责补充当前任务所需范围。

## 配套演示和工具
完整 ZIP 中的 `V2_START_HERE.md` 列出启动和工具命令。安装时 `PACKAGE_LOCATION.json` 记录资源包绝对位置；安装后的技能正文和契约可独立阅读，演示和集中工具仍在完整包中。不要假设聊天沙盒路径在用户机器存在。
