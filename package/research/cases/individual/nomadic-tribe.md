# Nomadic Tribe

- 案例 ID：`nomadic-tribe`
- 奖项：2019-02，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/nomadic-tribe

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2019-02。（s1: https://awwwards.com/nomadic-tribe-by-makemepulse-wins-site-of-the-month-february.html）
- 官方说明自研NanoGL做模块化材质与效果组合，Vue整合界面，WebAudio支持声音；制作先灰盒再替换最终资产。（s1: https://awwwards.com/nomadic-tribe-by-makemepulse-wins-site-of-the-month-february.html）
- 以插画和角色动画组织多章互动寓言。（s1: https://awwwards.com/nomadic-tribe-by-makemepulse-wins-site-of-the-month-february.html）
- 该历史版本的制作方资料列出：NanoGL。（s1: https://awwwards.com/nomadic-tribe-by-makemepulse-wins-site-of-the-month-february.html）
- 该历史版本的制作方资料列出：WebGL。（s1: https://awwwards.com/nomadic-tribe-by-makemepulse-wins-site-of-the-month-february.html）
- 该历史版本的制作方资料列出：WebAudio。（s1: https://awwwards.com/nomadic-tribe-by-makemepulse-wins-site-of-the-month-february.html）
- 该历史版本的制作方资料列出：Vue.js。（s1: https://awwwards.com/nomadic-tribe-by-makemepulse-wins-site-of-the-month-february.html）
- 该历史版本的制作方资料列出：Substance Painter。（s1: https://awwwards.com/nomadic-tribe-by-makemepulse-wins-site-of-the-month-february.html）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 把故事拆成章节、转场和用户动作三张表。
2. 用低模和纯色材质先验证节奏。
3. 为每种材质效果定义可复用参数，避免每场景复制整套shader。
4. 音频默认不播放；用户启用后提供持续可见静音控件。

**移动/异常回退**：保留语义DOM内容和明确可点控件；触屏不依赖悬停，reduced-motion跳过视觉位移；按本例验收条目提供对应静态/列表入口。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 快速跳章不重叠声音；静音和减弱动态不妨碍理解；读者随时回到章节目录。

**风险**

- 当前获奖版本与当前活站可能不同。
- 历史内部工具和旧API不可直接当作新项目依赖。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
