# Zentry

- 案例 ID：`zentry`
- 奖项：2024-08，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/zentry

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2024-08。（s1: https://www.awwwards.com/websites/sites_of_the_month/）
- 官方案例页列出Scrolling、Sound-Audio、Storytelling等标签，并提供产品、首页、品牌、序章、About交互片段。（s2: https://www.awwwards.com/sites/zentry）
- 官方页面没有列出React/GSAP等具体框架；网上教学克隆不等于原站源码。（s2: https://www.awwwards.com/sites/zentry）

## 分析推断：不可当作原作者源码声明

- 根据公开描述提炼的交互机制：章节式内容浏览
- 根据公开描述提炼的交互机制：产品分区展示
- 根据公开描述提炼的交互机制：叙事画面与大字配合

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 语义HTML章节包含产品信息
2. 原创视频用poster和lazy加载
3. 用clip-path与transform制作遮罩切换
4. 明确主CTA，不让特效吞没产品介绍

**移动/异常回退**：静态海报加短正文；提供播放/暂停；减少动效时显示完整章节。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 在触屏、键盘和reduced-motion三种输入/偏好下完成主任务。
- [ ] 静态海报加短正文；提供播放/暂停；减少动效时显示完整章节。
- [ ] 模拟媒体、网络或GPU加载失败时保留完整内容和导航。

**风险**

- 教学克隆误认原站技术
- 视频占用带宽
- 过度滚动接管

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
