---
name: awwwards-pattern-immersive-fallback
description: Implement a distinct immersive fallback pattern with recorded source-state observations, a standalone original example and explicit fallback, keyboard and lifecycle contracts.
---

# 沉浸式站点：图形增强失败时仍保留可用页面

## 用于什么任务
为相应页面增加此机制。它可以与 awwwards-page-external-home, awwwards-page-external-experiment, awwwards-3d-experience 配合；不要因此替换用户既有框架、品牌、接口或其他页面。

## 读取来源与限制
先读 [具体观察与配方](references/pattern-contract.json)。observed 是已记录的来源观察；recipe 是本库的原创实现方法；源站事实、推断和蓝本验证不得混用。

- 本轮匿名软件图形环境的实际截图出现了浏览器不支持的提示和静态视觉。
- 这是特定环境下的兼容回退观察，未验证该站正常图形体验，也不据此评价所有用户的浏览结果。

## 实施
1. 先以 DOM 交付项目、导航、说明和联系路径，图形层不得拥有唯一任务入口。
2. 增强层有初始化、静止、运动、暂停、回退和销毁状态；WebGL 初始化或 context loss 失败时可读内容保持可用。
3. 为当前增强实例记录资源所有权；卸载移除观察器、事件、动画帧并释放几何、材质与渲染器。
4. 限制 DPR、粒子和几何预算，提供轻量档；离屏和隐藏标签停帧，减少动画时仅绘制稳定视图。

## 不变量与验收
- 禁用 JavaScript、图形不可用或手动选择静态时，核心链接和项目文本仍在页面。
- 兼容失败不等于正常源站体验完成；原站技术版本与内部 shader 不得从图像猜测。
- 资源清理只释放当前实例所有的资源，不全局销毁其他页面。
- 原创建模与有许可的 Three.js 分开标记；保留 MIT 文本。
- 在 320/390/768/1440 宽度检查阅读顺序、主操作、溢出和焦点；实际操作主路径、失败恢复和减少动画路径。
- passed 需要本次运行证据；未执行的源站状态、真实设备或后端接入保留 not_run/blocked。

## 独立原创蓝本
```text
python scripts/scaffold.py --output YOUR_EMPTY_DIRECTORY
```
在导出目录运行 `python -m http.server 8000 --bind 127.0.0.1` 并访问 http://127.0.0.1:8000/ 。拒绝覆盖非空目录，不依赖 npm 或原站素材。Three.js 示例保留其 MIT 文件。

## 剩余边界
- 本轮源站正常三维交互未观察，示例为原创替代实现。
- 软件 WebGL 验证不能替代真实 GPU、手机和生产验收。

原站图像、字体、视频、音乐和标志不随技能分发。所有示例文案、几何和行为代码为原创；第三方库适用各自许可。
