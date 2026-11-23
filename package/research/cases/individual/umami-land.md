# Umami Land

- 案例 ID：`umami-land`
- 奖项：2021-02，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/umami-land

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2021-02。（s1: https://awwwards.com/umami-land-by-google-wins-site-of-the-month-february-2021.html）
- 制作方披露将静态内容合成一个2D球面，上叠动态3D对象；UI使用Vue，内容经Google Sheets API管理。（s1: https://awwwards.com/umami-land-by-google-wins-site-of-the-month-february-2021.html）
- 食物主题公园以热点引导用户了解菜品并访问相关搜索。（s1: https://awwwards.com/umami-land-by-google-wins-site-of-the-month-february-2021.html）
- 该历史版本的制作方资料列出：custom WebGL framework。（s1: https://awwwards.com/umami-land-by-google-wins-site-of-the-month-february-2021.html）
- 该历史版本的制作方资料列出：Vue.js。（s1: https://awwwards.com/umami-land-by-google-wins-site-of-the-month-february-2021.html）
- 该历史版本的制作方资料列出：GSAP。（s1: https://awwwards.com/umami-land-by-google-wins-site-of-the-month-february-2021.html）
- 该历史版本的制作方资料列出：Lottie。（s1: https://awwwards.com/umami-land-by-google-wins-site-of-the-month-february-2021.html）
- 该历史版本的制作方资料列出：Google Sheets API。（s1: https://awwwards.com/umami-land-by-google-wins-site-of-the-month-february-2021.html）
- 该历史版本的制作方资料列出：Google App Engine。（s1: https://awwwards.com/umami-land-by-google-wins-site-of-the-month-february-2021.html）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 建立菜品数据：标题、描述、图片、外链、语言。
2. 先做可搜索的DOM菜品列表，确保所有热点有对应列表项。
3. 静态背景与少量动态物体分层，逐区域加载。
4. 热点选择只改变介绍面板，打开外链由用户明确触发。

**移动/异常回退**：保留语义DOM内容和明确可点控件；触屏不依赖悬停，reduced-motion跳过视觉位移；按本例验收条目提供对应静态/列表入口。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 触控、键盘、列表三条路径得到同一菜品；外链可识别；无3D仍可搜索。

**风险**

- 当前获奖版本与当前活站可能不同。
- 历史内部工具和旧API不可直接当作新项目依赖。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
