# Bennett & Clive

- 案例 ID：`bennett-clive`
- 奖项：2024-03，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/bennett-clive

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2024-03。（s1: https://www.awwwards.com/bennett-clive.html）
- 制作方官方文章明确列出 Nuxt.js、GSAP、Netlify、Storyblok、Lenis。（s1: https://www.awwwards.com/bennett-clive.html；s2: https://www.awwwards.com/sites/bennett-clive）
- 交互式&符号作为品牌主体；作品页面强调内容，About页面更活跃。（s1: https://www.awwwards.com/bennett-clive.html；s2: https://www.awwwards.com/sites/bennett-clive）

## 分析推断：不可当作原作者源码声明

- 根据公开描述提炼的交互机制：&符号与相交元素产生视觉反应
- 根据公开描述提炼的交互机制：作品页和About采用不同动效密度

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 先建语义化内容与作品列表
2. 以SVG或DOM绘制原创品牌符号
3. 通过局部GSAP时间线更新相交效果
4. 路由切换统一dispose，保持返回位置

**移动/异常回退**：触屏不依赖hover；保留静态&与可点作品链接；reduced-motion直接呈现终态。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 在触屏、键盘和reduced-motion三种输入/偏好下完成主任务。
- [ ] 触屏不依赖hover；保留静态&与可点作品链接；reduced-motion直接呈现终态。
- [ ] 模拟媒体、网络或GPU加载失败时保留完整内容和导航。

**风险**

- 图形遮挡标题
- 大符号动态变形引发布局抖动
- 内容管理字段和动画状态耦合

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
