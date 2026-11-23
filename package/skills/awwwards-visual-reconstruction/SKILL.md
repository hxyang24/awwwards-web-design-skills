---
name: awwwards-visual-reconstruction
description: Rebuild authorized visual references through structured observation, original implementation and bounded screenshot comparison iterations.
---

# 视觉重建

保留布局思想与交互规律，使用已授权品牌素材和代码。目标是明确范围的重建，不保证一次完成任意网站。

## 输入与边界
读取用户目标、已有项目、允许修改的范围、目标设备和可用业务接口。缺省使用明确标识的本地样例；不要要求与当前任务无关的部署、审批或配置。

## 执行
1. 输入 reference-brief 与已有项目约束，先做关键区域和主路径。
2. 将内容、布局、tokens、组件与动画拆开，避免截图绝对坐标拼贴。
3. 按相同 viewport、DPR、浏览器、字体和状态截图。
4. 运行 visual_diff.mjs 输出像素差与差异图，再人工看关键区域。
5. 最多按约定迭代预算修复；记录剩余差异、未知交互和未授权素材替代。

## 交付与检查
输出 reconstruction-log、candidate screenshots、diff report 与交互测试。内置原创参照卡可用于正负例重建演练。

根据任务读取 [专项执行契约](references/contract.md)。如与原有 V1 技能共同使用，保留已有脚本和接口；V2 负责补充当前任务所需范围。

## 配套演示和工具
完整 ZIP 中的 `V2_START_HERE.md` 列出启动和工具命令。安装时 `PACKAGE_LOCATION.json` 记录资源包绝对位置；安装后的技能正文和契约可独立阅读，演示和集中工具仍在完整包中。不要假设聊天沙盒路径在用户机器存在。
