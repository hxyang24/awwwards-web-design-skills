# Bruno Simon Portfolio

- 案例 ID：`bruno-simon-portfolio`
- 奖项：2019-11，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/bruno-simon-portfolio

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2019-11。（s1: https://awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html）
- 2019年官方案例明确使用Three.js渲染、Cannon.js物理；可见低模与物理简化体分离，并有移动控制。（s1: https://awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html）
- 用俯视小车游戏连接个人信息、项目和联系区域。（s1: https://awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html）
- 该历史版本的制作方资料列出：Three.js。（s1: https://awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html）
- 该历史版本的制作方资料列出：Cannon.js。（s1: https://awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html）
- 该历史版本的制作方资料列出：Blender。（s1: https://awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html）
- 该历史版本的制作方资料列出：glTF。（s1: https://awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html）
- 该历史版本的制作方资料列出：Draco。（s1: https://awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 先写常规作品列表和联系信息。
2. 灰盒场景只放一辆车、一个碰撞体和一个项目热点。
3. 物理世界和渲染世界保持单向同步；固定步长处理物理。
4. 提供触摸控制、暂停、重置与跳过游戏入口。

**移动/异常回退**：保留语义DOM内容和明确可点控件；触屏不依赖悬停，reduced-motion跳过视觉位移；按本例验收条目提供对应静态/列表入口。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 非玩家不驾驶也能找到项目与联系；后台标签页暂停；长时间卡住能重置。

**风险**

- 当前获奖版本与当前活站可能不同。
- 历史内部工具和旧API不可直接当作新项目依赖。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
