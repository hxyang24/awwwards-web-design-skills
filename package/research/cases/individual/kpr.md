# KPR

- 案例 ID：`kpr`
- 奖项：2022-12，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/kpr

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2022-12。（s1: https://awwwards.com/kpr-by-resn-wins-sotm.html）
- 官方描述：SDF与精灵图用于加载揭示，Stencil Buffer让一个3D场景遮罩另一个；按住层的图形通过CSS变换定位。（s1: https://awwwards.com/kpr-by-resn-wins-sotm.html）
- 滚动探索虚构世界，按住指针揭示第二层叙事。（s1: https://awwwards.com/kpr-by-resn-wins-sotm.html）
- 该历史版本的制作方资料列出：WebGL。（s1: https://awwwards.com/kpr-by-resn-wins-sotm.html）
- 该历史版本的制作方资料列出：HTML。（s1: https://awwwards.com/kpr-by-resn-wins-sotm.html）
- 该历史版本的制作方资料列出：CSS transforms。（s1: https://awwwards.com/kpr-by-resn-wins-sotm.html）
- 该历史版本的制作方资料列出：After Effects。（s1: https://awwwards.com/kpr-by-resn-wins-sotm.html）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 将章节、热点和次级信息保存为独立数据。
2. 先实现DOM章节与可点击“显示更多”，再加入WebGL遮罩。
3. 为pointerdown/up/cancel、blur和键盘Enter/Space建立同一状态机。
4. 每次离开章节恢复未按下状态，暂停不可见场景。

**移动/异常回退**：保留语义DOM内容和明确可点控件；触屏不依赖悬停，reduced-motion跳过视觉位移；按本例验收条目提供对应静态/列表入口。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 按住与点击切换均能读到同一信息；取消指针和失焦不遗留遮罩；无WebGL仍有全部正文。

**风险**

- 当前获奖版本与当前活站可能不同。
- 历史内部工具和旧API不可直接当作新项目依赖。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
