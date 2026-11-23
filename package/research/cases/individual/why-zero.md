# Why Zero

- 案例 ID：`why-zero`
- 奖项：2026-09，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/why-zero

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2026-09。（s1: https://www.awwwards.com/websites/sites_of_the_month/）
- 制作方BUNQ LABS明确WebGL/Three.js/shader工程，Blender预烘焙照明、按帧率调整视觉质量，目标包含低价旧Android。（s2: https://www.awwwards.com/sites/why-zero；s3: https://bunqlabs.com/insights/why-zero-awards）
- 制作方描述画零破冰、六阶段滚动、穿过logo隧道到探索城市。（s2: https://www.awwwards.com/sites/why-zero；s3: https://bunqlabs.com/insights/why-zero-awards）
- 制作方提供流量/FPS/体积自述，本记录不把它们当作独立实测。（s2: https://www.awwwards.com/sites/why-zero；s3: https://bunqlabs.com/insights/why-zero-awards）

## 分析推断：不可当作原作者源码声明

- 根据公开描述提炼的交互机制：开场画零
- 根据公开描述提炼的交互机制：连续叙事章节
- 根据公开描述提炼的交互机制：最终城市探索

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 开场提供跳过
2. 故事内容与动画时间线分离
3. 预烘焙照明/压缩纹理
4. 按持续帧时间降DPR和后处理，保持内容与导航

**移动/异常回退**：提供无需绘画的进入按钮与顺序章节；低性能设备使用静态内容；降低画质而不删教育信息。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 在触屏、键盘和reduced-motion三种输入/偏好下完成主任务。
- [ ] 提供无需绘画的进入按钮与顺序章节；低性能设备使用静态内容；降低画质而不删教育信息。
- [ ] 模拟媒体、网络或GPU加载失败时保留完整内容和导航。

**风险**

- 交互入口阻塞
- 温度与耗电
- 不可验证的制作方性能宣传
- 只测单一Android代表全部设备

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
