# Oryzo AI

- 案例 ID：`oryzo-ai`
- 奖项：2026-04，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/oryzo-ai

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2026-04。（s1: https://www.awwwards.com/websites/sites_of_the_month/）
- Lusion第一方说明这是把软木杯垫包装为AI时代产品的自发项目，并非真实AI软件。（s2: https://www.awwwards.com/sites/oryzo-ai；s3: https://lusion.co/projects/oryzo_ai；s4: https://blog.lusion.co/oryzo-bts-part-3-7-website-ux-ui-and-illustrations）
- 官方项目服务列出WebGL、3D Design、Animation。（s2: https://www.awwwards.com/sites/oryzo-ai；s3: https://lusion.co/projects/oryzo_ai；s4: https://blog.lusion.co/oryzo-bts-part-3-7-website-ux-ui-and-illustrations）
- 设计幕后文章说明实时3D、少量字体/颜色、手绘插画；Figma用于设计，Rive用于交互原型；不等于生产站Rive依赖。（s2: https://www.awwwards.com/sites/oryzo-ai；s3: https://lusion.co/projects/oryzo_ai；s4: https://blog.lusion.co/oryzo-bts-part-3-7-website-ux-ui-and-illustrations）

## 分析推断：不可当作原作者源码声明

- 根据公开描述提炼的交互机制：真实桌面作为首页场景
- 根据公开描述提炼的交互机制：产品贯穿叙事
- 根据公开描述提炼的交互机制：场景连续过渡
- 根据公开描述提炼的交互机制：手绘插画构成视觉细节

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 为真实业务明确产品价值再选叙事道具
2. 以滚动章节映射同一产品状态
3. 保持标题/价格/说明DOM可读
4. 实验与真实产品能力文案分开

**移动/异常回退**：用产品静态图和短片；减少动效显示完整功能说明；不让幽默掩盖真实购买条件。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 在触屏、键盘和reduced-motion三种输入/偏好下完成主任务。
- [ ] 用产品静态图和短片；减少动效显示完整功能说明；不让幽默掩盖真实购买条件。
- [ ] 模拟媒体、网络或GPU加载失败时保留完整内容和导航。

**风险**

- 把名称AI误分类为SaaS
- 原型工具误当生产依赖
- 长叙事拖慢获取信息

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
