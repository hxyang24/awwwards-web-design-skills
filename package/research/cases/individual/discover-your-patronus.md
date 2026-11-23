# Discover Your Patronus

- 案例 ID：`discover-your-patronus`
- 奖项：2016-10，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/discover-your-patronus

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2016-10。（s1: https://www.awwwards.com/websites/sites_of_the_month/?page=4）
- 官方作品说明用户在3D环境中按提示选择并揭晓结果。（s2: https://www.awwwards.com/sites/discover-your-patronus；s3: https://www.rafaeldante.com/project/graveyard）
- 参与者Rafael Dante确认WebGL体验和Awwwards SOTM。（s2: https://www.awwwards.com/sites/discover-your-patronus；s3: https://www.rafaeldante.com/project/graveyard）
- Awwwards作品页标签包括WebGL、Three.js、GLSL；结果映射算法与版本未知。（s2: https://www.awwwards.com/sites/discover-your-patronus；s3: https://www.rafaeldante.com/project/graveyard）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 先用DOM实现问答状态机。
2. 摄像机订阅业务状态，动画不能成为提交答案的唯一途径。
3. 选择后锁定重复提交，并提供键盘等价输入。
4. GPU失败时保留完整DOM问答与结果页。

**移动/异常回退**：采用本例步骤与验收中的DOM、静态图、触摸按钮或鼠标替代路径；图形增强失败时主任务仍可完成。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 覆盖重复点击、返回、刷新与超时。
- [ ] 无WebGL仍能完成流程。
- [ ] 低动态偏好保留全部文本。

**风险**

- 历史站点可能不可运行。
- 输入设备和浏览器能力变化需要重新验收。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
