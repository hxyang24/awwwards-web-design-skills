# Igloo Inc

- 案例 ID：`igloo-inc`
- 奖项：2024-未知，状态：`unresolved`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/igloo-inc

## 有来源的公开事实

- 该案例收录于官方月度档案；本次核验未确定2024年的具体月度获奖月份。（s1: https://www.awwwards.com/websites/sites_of_the_month/）
- abeto官方文章明确列出Three.js、Svelte、GSAP、Vite、Houdini、Blender等。（s2: https://www.awwwards.com/sites/igloo-inc；s3: https://www.awwwards.com/igloo-inc-case-study.html）
- 文章描述程序化冰晶建模、VDB体积数据导出与压缩、WebGL文字/SDF、分阶段加载和着色器编译。（s2: https://www.awwwards.com/sites/igloo-inc；s3: https://www.awwwards.com/igloo-inc-case-study.html）

## 分析推断：不可当作原作者源码声明

- 根据公开描述提炼的交互机制：滚动驱动镜头穿越冰块
- 根据公开描述提炼的交互机制：粒子形成不同链接对应形状
- 根据公开描述提炼的交互机制：文字故障与扰动

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 先用灰盒验证三章节镜头路径
2. 把正文与链接保留DOM
3. 将重型场景作延迟增强
4. 预编译下一场景并释放已完成资源

**移动/异常回退**：原始内容为可读三节页面；无WebGL或reduced-motion显示三张静态图；链接照常可操作。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 在触屏、键盘和reduced-motion三种输入/偏好下完成主任务。
- [ ] 原始内容为可读三节页面；无WebGL或reduced-motion显示三张静态图；链接照常可操作。
- [ ] 模拟媒体、网络或GPU加载失败时保留完整内容和导航。

**风险**

- 全Canvas文字可访问性
- GPU显存
- 首屏编译卡顿
- 程序化美术成本

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
