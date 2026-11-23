---
name: awwwards-fintech
description: Design market and order interfaces with precise amounts, quote freshness, review and confirmation, order state and explicit simulation boundaries.
---

# 金融交易终端

先定义价格单位、交易数量、币种、报价时间和订单状态机。演示不能显示真实成交、余额变更或资金已到账。

## 输入与边界
读取用户目标、已有项目、允许修改的范围、目标设备和可用业务接口。缺省使用明确标识的本地样例；不要要求与当前任务无关的部署、审批或配置。

## 执行
1. 从持牌数据或授权 API 读取报价；注明延迟、时区和交易时段。
2. 整数分或十进制定点计算金额，逐市场定义 tick、lot、费用和舍入。
3. 报价过期、超额、无权限、风控失败时拒绝审阅。
4. 二次确认绑定订单摘要和报价版本；内容变化后重新审阅。
5. 撤单、部分成交与重试由服务端状态决定，不能仅本地改标签。

## 交付与检查
输出 order-state-machine、money-contract、quote-contract、risk-checklist 和模拟/真实边界。Axis 演示只支持 USD 整股限价买单。

根据任务读取 [专项执行契约](references/contract.md)。如与原有 V1 技能共同使用，保留已有脚本和接口；V2 负责补充当前任务所需范围。

## 配套演示和工具
完整 ZIP 中的 `V2_START_HERE.md` 列出启动和工具命令。安装时 `PACKAGE_LOCATION.json` 记录资源包绝对位置；安装后的技能正文和契约可独立阅读，演示和集中工具仍在完整包中。不要假设聊天沙盒路径在用户机器存在。
