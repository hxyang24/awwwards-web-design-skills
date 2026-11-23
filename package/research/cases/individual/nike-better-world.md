# Nike Better World

- 案例 ID：`nike-better-world`
- 奖项：2011-01，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/nike-better-world

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2011-01。（s1: https://www.awwwards.com/websites/sites_of_the_month/?page=7）
- 官方作品页列出Parallax与Big Background Images标签，主题为通过运动创造更美好的世界。（s2: https://www.awwwards.com/sites/nike-better-world）
- 可核验视差交互类别；框架、版本与CMS未知。（s2: https://www.awwwards.com/sites/nike-better-world）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 先用语义section交付完整静态内容。
2. 将前后景设为不同位移系数，保持阅读顺序。
3. 每帧集中读取滚动状态并更新transform。
4. reduced-motion取消位移，手机端提供静态构图。

**移动/异常回退**：采用本例步骤与验收中的DOM、静态图、触摸按钮或鼠标替代路径；图形增强失败时主任务仍可完成。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 禁用JS仍可读。
- [ ] 键盘锚点可直接访问各节。
- [ ] 320px与1440px无正文溢出。

**风险**

- 历史站点可能不可运行。
- 输入设备和浏览器能力变化需要重新验收。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
