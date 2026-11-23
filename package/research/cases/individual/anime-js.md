# Anime.js

- 案例 ID：`anime-js`
- 奖项：2025-05，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/anime-js

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2025-05。（s1: https://www.awwwards.com/websites/sites_of_the_month/）
- 作者官方Learn页明确其落地页重建会使用HTML、CSS、SVG、Canvas 2D和WebGL(Three.js)。（s2: https://www.awwwards.com/sites/anime-js；s3: https://animejs.com/learn）
- 官方Awwwards页描述该产品为JavaScript动画库。（s2: https://www.awwwards.com/sites/anime-js；s3: https://animejs.com/learn）

## 分析推断：不可当作原作者源码声明

- 根据公开描述提炼的交互机制：动画示例本身构成产品演示
- 根据公开描述提炼的交互机制：不同渲染媒介展示能力

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 用少量独立演示对应API能力
2. 演示包含暂停/重播
3. 使用既有锁文件确定Anime.js API版本
4. 将代码示例与动态效果并排

**移动/异常回退**：精简复杂示例并提供录屏/静态终态；API代码和文档始终可读。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 在触屏、键盘和reduced-motion三种输入/偏好下完成主任务。
- [ ] 精简复杂示例并提供录屏/静态终态；API代码和文档始终可读。
- [ ] 模拟媒体、网络或GPU加载失败时保留完整内容和导航。

**风险**

- v3/v4 API混用
- 多个演示同时运行
- 把计划课程误当公开完整源码

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
