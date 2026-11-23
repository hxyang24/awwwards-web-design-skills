---
name: awwwards-3d-experience
description: Build progressive Three.js and WebGL scenes with resource ownership, quality budgets, context-loss handling and readable fallback.
---

# WebGL 与 3D

三维是增强层。网页正文和主操作保留在 DOM；渲染器失效、设备过热或减少动画时仍可完成任务。

## 输入与边界
读取用户目标、已有项目、允许修改的范围、目标设备和可用业务接口。缺省使用明确标识的本地样例；不要要求与当前任务无关的部署、审批或配置。

## 执行
1. 明确场景、相机、网格、灯光与每种资源的所有者。
2. 设 DPR 上限、几何面数、纹理体积和质量档；避免无上限像素比。
3. 离屏和隐藏标签暂停更新；减少动画静止渲染或退回静态。
4. 卸载移除监听器、取消循环并释放 geometry/material/texture/render target。
5. 处理 context lost；多次进入退出检查释放次数和不增长的资源。

## 交付与检查
输出 scene-budget、resource-ledger、fallback-spec、GPU 验证条件。Orbit 是真实几何体演示，不包含通用物理世界或任意 shader 复现。

根据任务读取 [专项执行契约](references/contract.md)。如与原有 V1 技能共同使用，保留已有脚本和接口；V2 负责补充当前任务所需范围。

## 配套演示和工具
完整 ZIP 中的 `V2_START_HERE.md` 列出启动和工具命令。安装时 `PACKAGE_LOCATION.json` 记录资源包绝对位置；安装后的技能正文和契约可独立阅读，演示和集中工具仍在完整包中。不要假设聊天沙盒路径在用户机器存在。
