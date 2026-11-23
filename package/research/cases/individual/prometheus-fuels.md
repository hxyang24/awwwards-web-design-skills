# Prometheus Fuels

- 案例 ID：`prometheus-fuels`
- 奖项：2021-05，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/prometheus-fuels

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2021-05。（s1: https://www.awwwards.com/prometheus-by-active-theory-wins-site-of-the-month-may-2021.html）
- 官方披露每场景起止相机的可调系统、边缘噪声处理及转场时交替渲染场景的性能策略。（s1: https://www.awwwards.com/prometheus-by-active-theory-wins-site-of-the-month-may-2021.html）
- 用复古未来视觉和滚动章节解释燃料技术。（s1: https://www.awwwards.com/prometheus-by-active-theory-wins-site-of-the-month-may-2021.html）
- 该历史版本的制作方资料列出：custom 3D engine。（s1: https://www.awwwards.com/prometheus-by-active-theory-wins-site-of-the-month-may-2021.html）
- 该历史版本的制作方资料列出：WebGL-style shader pipeline。（s1: https://www.awwwards.com/prometheus-by-active-theory-wins-site-of-the-month-may-2021.html）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 用明确文本说明技术输入、过程、输出与证据边界。
2. 给每章保存起止相机与动画参数，允许可视调参。
3. 按实际设备测试转场开销，再选择冻结、交替渲染或预渲染。
4. 交互提示必须附可点击控件，避免只支持空格键。

**移动/异常回退**：保留语义DOM内容和明确可点控件；触屏不依赖悬停，reduced-motion跳过视觉位移；按本例验收条目提供对应静态/列表入口。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 快速滚动、反向滚动和跳章无黑屏；图形失败仍可读技术说明；所有环保及性能宣称有来源。

**风险**

- 当前获奖版本与当前活站可能不同。
- 历史内部工具和旧API不可直接当作新项目依赖。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
