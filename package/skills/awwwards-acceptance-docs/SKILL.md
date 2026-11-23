---
name: awwwards-acceptance-docs
description: Create evidence-linked acceptance and handoff documents separating implementation, runtime tests, production integration and untested scope.
---

# 验收与文档

passed 必须指向这次实际运行的证据。旧版报告是历史证据；本地浏览器测试不等于生产、安全、真机或现场验收。

## 输入与边界
读取用户目标、已有项目、允许修改的范围、目标设备和可用业务接口。缺省使用明确标识的本地样例；不要要求与当前任务无关的部署、审批或配置。

## 执行
1. 定义用户主路径、状态矩阵、目标设备和必要的工程检查。
2. 运行静态、逻辑、浏览器、无障碍和视觉检查，逐项记录范围。
3. 失败保留输出与修复后的新证据；blocked/not_run 不能改成 passed。
4. 报告支持证据路径、哈希、命令、环境和限制；性能分实验室/真实用户。
5. 交付校验清单、启动方式、依赖锁、版权台账和未完成集成。

## 交付与检查
输出 acceptance.json 与 HANDOFF.md。生产验收、真实支付/交易/模型、真机和完整 WCAG 审计需独立执行。

根据任务读取 [专项执行契约](references/contract.md)。如与原有 V1 技能共同使用，保留已有脚本和接口；V2 负责补充当前任务所需范围。

## 配套演示和工具
完整 ZIP 中的 `V2_START_HERE.md` 列出启动和工具命令。安装时 `PACKAGE_LOCATION.json` 记录资源包绝对位置；安装后的技能正文和契约可独立阅读，演示和集中工具仍在完整包中。不要假设聊天沙盒路径在用户机器存在。
