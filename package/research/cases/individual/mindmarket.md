# MindMarket

- 案例 ID：`mindmarket`
- 奖项：2025-12，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/mindmarket

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2025-12。（s1: https://www.awwwards.com/websites/sites_of_the_month/）
- KOKI-KIKO官方案例明确Astro、DatoCMS、Netlify、Tailwind CSS、Rive、GSAP DrawSVG、Locomotive Scroll(基于Lenis)。（s2: https://www.awwwards.com/sites/mindmarket；s3: https://www.awwwards.com/mindmarket-case-study.html）
- Rive由IntersectionObserver触发；首页线条由三层路径形成。（s2: https://www.awwwards.com/sites/mindmarket；s3: https://www.awwwards.com/mindmarket-case-study.html）
- 滚动进度0到1驱动暂停的GSAP时间线。（s2: https://www.awwwards.com/sites/mindmarket；s3: https://www.awwwards.com/mindmarket-case-study.html）

## 分析推断：不可当作原作者源码声明

- 根据公开描述提炼的交互机制：滚动绘制连接线
- 根据公开描述提炼的交互机制：角色进入视口触发
- 根据公开描述提炼的交互机制：插画随断点人工排布

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. SVG路径在各断点单独设计
2. 进度归一化驱动动画
3. observer负责启停Rive
4. 静态插画保底并保留正文自然文档流

**移动/异常回退**：小屏路径简化；减少动效时显示完整线与静态角色；停止离屏和后台动画。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 在触屏、键盘和reduced-motion三种输入/偏好下完成主任务。
- [ ] 小屏路径简化；减少动效时显示完整线与静态角色；停止离屏和后台动画。
- [ ] 模拟媒体、网络或GPU加载失败时保留完整内容和导航。

**风险**

- 路径与文字错位
- 误用固定像素导致溢出
- 多个运行时循环叠加

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
