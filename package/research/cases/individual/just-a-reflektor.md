# Just A Reflektor

- 案例 ID：`just-a-reflektor`
- 奖项：2013-09，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/just-a-reflektor

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2013-09。（s1: https://www.awwwards.com/websites/sites_of_the_month/?page=6）
- Google实验页说明项目已不活跃。（s2: https://www.awwwards.com/sites/just-a-reflektor；s3: https://experiments.withgoogle.com/just-a-reflektor；s4: https://archive.unit9.com/project/reflektor/；s5: https://github.com/unit9/justareflektor）
- UNIT9说明手机动作实时修改视频视觉效果。（s2: https://www.awwwards.com/sites/just-a-reflektor；s3: https://experiments.withgoogle.com/just-a-reflektor；s4: https://archive.unit9.com/project/reflektor/；s5: https://github.com/unit9/justareflektor）
- 制作方明确使用WebSocket交换陀螺仪和加速度计数据，并以摄像头定位手机。（s2: https://www.awwwards.com/sites/just-a-reflektor；s3: https://experiments.withgoogle.com/just-a-reflektor；s4: https://archive.unit9.com/project/reflektor/；s5: https://github.com/unit9/justareflektor）
- Google确认WebGL，并提供开源代码入口。（s2: https://www.awwwards.com/sites/just-a-reflektor；s3: https://experiments.withgoogle.com/just-a-reflektor；s4: https://archive.unit9.com/project/reflektor/；s5: https://github.com/unit9/justareflektor）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 先做鼠标可控shader，再增加手机配对。
2. 输入归一化为独立input-state，UI不直接操控shader。
3. 为传感器拒绝、相机不可用、配对失败分别提供回退。
4. 限频、平滑网络输入，超时停止控制。

**移动/异常回退**：采用本例步骤与验收中的DOM、静态图、触摸按钮或鼠标替代路径；图形增强失败时主任务仍可完成。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 拒绝权限仍能用鼠标/触摸完成。
- [ ] 配对凭证隔离会话。
- [ ] 暂停视频同时暂停视觉时钟。

**风险**

- 历史站点可能不可运行。
- 输入设备和浏览器能力变化需要重新验收。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
