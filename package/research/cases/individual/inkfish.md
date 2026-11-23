# Inkfish

- 案例 ID：`inkfish`
- 奖项：2024-05，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/inkfish

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2024-05。（s1: https://www.awwwards.com/websites/sites_of_the_month/）
- DashDigital说明使用单一Canvas 2D绘制双视频以同步首屏画面。（s2: https://www.awwwards.com/sites/inkfish；s3: https://dashdigital.studio/case-studies/inkfish）
- 制作方说明React hooks管理视频加载，React Transition Group管理路由过渡，开发范围包含React/Next.js。（s2: https://www.awwwards.com/sites/inkfish；s3: https://dashdigital.studio/case-studies/inkfish）
- 压缩MP4通过Vimeo直链分发；提供移动视频版本；作品卡片hover时加载。（s2: https://www.awwwards.com/sites/inkfish；s3: https://dashdigital.studio/case-studies/inkfish）

## 分析推断：不可当作原作者源码声明

- 根据公开描述提炼的交互机制：双视频同步
- 根据公开描述提炼的交互机制：悬停作品预览
- 根据公开描述提炼的交互机制：全屏播放器与时间轴截图预览
- 根据公开描述提炼的交互机制：页面块状故障转场

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 用一个媒体时钟驱动画布合成
2. 可见后启用预览并中止离屏播放
3. 模态框通过portal挂载并实现焦点管理
4. 转场仅遮盖内容准备过程，设置超时与取消

**移动/异常回退**：无hover时点选预览；弱网使用poster；全屏播放器保留原生controls替代。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 在触屏、键盘和reduced-motion三种输入/偏好下完成主任务。
- [ ] 无hover时点选预览；弱网使用poster；全屏播放器保留原生controls替代。
- [ ] 模拟媒体、网络或GPU加载失败时保留完整内容和导航。

**风险**

- Canvas抽帧跨域限制
- 双视频解码耗电
- 音频自动播放限制
- 全屏模态焦点陷阱

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
