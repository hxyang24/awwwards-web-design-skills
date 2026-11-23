---
name: awwwards-visual-diff
description: Measure screenshot pixel differences with strict dimensions, explicit masks and region thresholds while retaining manual visual review.
---

# 视觉差异评估

尺寸不一致直接失败，不自动缩放掩盖错误。像素相似只能用于回归判断，不能单独证明设计质量或业务正确。

## 输入与边界
读取用户目标、已有项目、允许修改的范围、目标设备和可用业务接口。缺省使用明确标识的本地样例；不要要求与当前任务无关的部署、审批或配置。

## 执行
1. 固定浏览器、操作系统、字体、DPR、语言、动画和数据时钟。
2. 对每张参照给出来源、批准者与阈值；禁止直接更新基准让失败通过。
3. mask 仅限已声明动态区域；关键 CTA、金额、错误提示禁止遮罩。
4. 输出 diff PNG、changed ratio、平均通道差与区域独立结果。
5. 同时测试相同图通过、结构变动失败、尺寸失败与区域差异；人工复核关键差异。

## 交付与检查
输出 visual-diff.json、diff.png 与 baseline-approval。工具支持 JSON 配置的 regions 和 masks；样例阈值须按项目约定。

根据任务读取 [专项执行契约](references/contract.md)。如与原有 V1 技能共同使用，保留已有脚本和接口；V2 负责补充当前任务所需范围。

## 配套演示和工具
完整 ZIP 中的 `V2_START_HERE.md` 列出启动和工具命令。安装时 `PACKAGE_LOCATION.json` 记录资源包绝对位置；安装后的技能正文和契约可独立阅读，演示和集中工具仍在完整包中。不要假设聊天沙盒路径在用户机器存在。
