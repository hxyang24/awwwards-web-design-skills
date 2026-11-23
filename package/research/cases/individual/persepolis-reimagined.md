# Persepolis Reimagined

- 案例 ID：`persepolis-reimagined`
- 奖项：2022-06，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/persepolis-reimagined

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2022-06。（s1: https://awwwards.com/case-study-getty-persepolis-reimagined.html）
- 官方披露了视频与实时场景对齐、视锥剔除、LOD、动态实例化及Unity场景导出到自定义JSON的制作流程。（s1: https://awwwards.com/case-study-getty-persepolis-reimagined.html）
- 从电影式开场进入可探索的古城，地图和章节共用视觉风格。（s1: https://awwwards.com/case-study-getty-persepolis-reimagined.html）
- 该历史版本的制作方资料列出：WebGL 2。（s1: https://awwwards.com/case-study-getty-persepolis-reimagined.html）
- 该历史版本的制作方资料列出：Vue.js。（s1: https://awwwards.com/case-study-getty-persepolis-reimagined.html）
- 该历史版本的制作方资料列出：GSAP。（s1: https://awwwards.com/case-study-getty-persepolis-reimagined.html）
- 该历史版本的制作方资料列出：Unity。（s1: https://awwwards.com/case-study-getty-persepolis-reimagined.html）
- 该历史版本的制作方资料列出：Maya。（s1: https://awwwards.com/case-study-getty-persepolis-reimagined.html）
- 该历史版本的制作方资料列出：Substance Painter。（s1: https://awwwards.com/case-study-getty-persepolis-reimagined.html）
- 该历史版本的制作方资料列出：After Effects。（s1: https://awwwards.com/case-study-getty-persepolis-reimagined.html）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 把史实、复原假设和参考图分开登记。
2. 建立固定相机路径和低模灰盒；只给可见范围制作细节。
3. 将重复构件实例化并按可见性剔除；用法线贴图替代不必要几何。
4. 为视频切入实时场景保存同一相机、色彩与时间基准。

**移动/异常回退**：保留语义DOM内容和明确可点控件；触屏不依赖悬停，reduced-motion跳过视觉位移；按本例验收条目提供对应静态/列表入口。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 低配模式能进入章节；地图可键盘选点；实时场景失败时静态图与文字可完成阅读。

**风险**

- 当前获奖版本与当前活站可能不同。
- 历史内部工具和旧API不可直接当作新项目依赖。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
