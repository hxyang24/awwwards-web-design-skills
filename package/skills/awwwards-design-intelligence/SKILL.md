---
name: awwwards-design-intelligence
description: Extract evidence-backed layout, color and component specifications from authorized screenshots or observed websites.
---

# 截图与网站参照分析

先建立证据台账再推断。单张截图无法证明字体身份、响应式断点、隐藏交互、后台接口或资源许可。

## 输入与边界
读取用户目标、已有项目、允许修改的范围、目标设备和可用业务接口。缺省使用明确标识的本地样例；不要要求与当前任务无关的部署、审批或配置。

## 执行
1. 记录截图来源、授权范围、时间、viewport、DPR、页面和交互状态。
2. 按区域测量边界、基线、留白、字号角色和色彩分布。
3. 用 inspect_image.mjs 提取尺寸和量化主色；文字识别与字体判断仍需人工核验。
4. 可访问网站仅观察已授权页面和交互，不绕过登录付费或下载受保护资源。
5. 输出 observations 与 hypotheses；不能把推断写为源码事实。

## 交付与检查
输出 reference-brief.json、资产许可台账与缺失状态。工具只能辅助测量，不能自动完整理解任意网站。

根据任务读取 [专项执行契约](references/contract.md)。如与原有 V1 技能共同使用，保留已有脚本和接口；V2 负责补充当前任务所需范围。

## 配套演示和工具
完整 ZIP 中的 `V2_START_HERE.md` 列出启动和工具命令。安装时 `PACKAGE_LOCATION.json` 记录资源包绝对位置；安装后的技能正文和契约可独立阅读，演示和集中工具仍在完整包中。不要假设聊天沙盒路径在用户机器存在。
