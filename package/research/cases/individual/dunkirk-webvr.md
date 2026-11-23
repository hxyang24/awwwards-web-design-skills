# Dunkirk WebVR

- 案例 ID：`dunkirk-webvr`
- 奖项：2017-07，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/dunkirk-webvr

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2017-07。（s1: https://www.awwwards.com/jam3-wins-site-of-the-month-july-with-dunkirk-webvr.html）
- 2017年官方案例说明不同玩家视角、凝视交互、空间音效、雾着色器及DOM文字转WebGL纹理。（s1: https://www.awwwards.com/jam3-wins-site-of-the-month-july-with-dunkirk-webvr.html）
- 双人合作的360度体验以凝视操作和声音方向建立紧张感。（s1: https://www.awwwards.com/jam3-wins-site-of-the-month-july-with-dunkirk-webvr.html）
- 该历史版本的制作方资料列出：WebVR。（s1: https://www.awwwards.com/jam3-wins-site-of-the-month-july-with-dunkirk-webvr.html）
- 该历史版本的制作方资料列出：WebGL textures。（s1: https://www.awwwards.com/jam3-wins-site-of-the-month-july-with-dunkirk-webvr.html）
- 该历史版本的制作方资料列出：custom fog shader。（s1: https://www.awwwards.com/jam3-wins-site-of-the-month-july-with-dunkirk-webvr.html）
- 该历史版本的制作方资料列出：spatial audio。（s1: https://www.awwwards.com/jam3-wins-site-of-the-month-july-with-dunkirk-webvr.html）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 先定义单人可运行的状态机和每步任务。
2. 把每个凝视动作配套按钮、键盘和触控操作。
3. 多人同步只发送离散状态变化，记录超时、断线、重连与离开。
4. 使用当前项目支持的XR接口；旧WebVR作为历史研究保留。

**移动/异常回退**：保留语义DOM内容和明确可点控件；触屏不依赖悬停，reduced-motion跳过视觉位移；按本例验收条目提供对应静态/列表入口。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 缺第二玩家可退出或进入单人介绍；网络中断明确说明；非XR设备有平面替代。

**风险**

- 当前获奖版本与当前活站可能不同。
- 历史内部工具和旧API不可直接当作新项目依赖。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
