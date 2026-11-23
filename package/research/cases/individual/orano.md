# Orano

- 案例 ID：`orano`
- 奖项：2018-11，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/orano

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2018-11。（s1: https://awwwards.com/orano-from-immersive-garden-wins-site-of-the-month-novemeber.html）
- 官方披露Blender边线导出和自定义OBJ解析、重复地形变换、移动简化网格以及Vue界面。（s1: https://awwwards.com/orano-from-immersive-garden-wins-site-of-the-month-novemeber.html）
- 每种工业产品以独立场景解释，滚动结尾用小交互演示用途。（s1: https://awwwards.com/orano-from-immersive-garden-wins-site-of-the-month-novemeber.html）
- 该历史版本的制作方资料列出：Three.js。（s1: https://awwwards.com/orano-from-immersive-garden-wins-site-of-the-month-novemeber.html）
- 该历史版本的制作方资料列出：WebGL。（s1: https://awwwards.com/orano-from-immersive-garden-wins-site-of-the-month-novemeber.html）
- 该历史版本的制作方资料列出：Blender。（s1: https://awwwards.com/orano-from-immersive-garden-wins-site-of-the-month-novemeber.html）
- 该历史版本的制作方资料列出：Vue.js。（s1: https://awwwards.com/orano-from-immersive-garden-wins-site-of-the-month-novemeber.html）
- 该历史版本的制作方资料列出：Stylus。（s1: https://awwwards.com/orano-from-immersive-garden-wins-site-of-the-month-novemeber.html）
- 该历史版本的制作方资料列出：Webpack。（s1: https://awwwards.com/orano-from-immersive-garden-wins-site-of-the-month-novemeber.html）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 先把产品任务、应用限制和可验证收益写成产品卡。
2. 每个产品只选择一个用户动作说明一个工作原理。
3. 需要线框时优先离线导出所需边，避免高成本运行时生成。
4. 复用地形与材质，移动端替换简化资源；保留直接询价入口。

**移动/异常回退**：保留语义DOM内容和明确可点控件；触屏不依赖悬停，reduced-motion跳过视觉位移；按本例验收条目提供对应静态/列表入口。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 用户可跳过场景进入产品说明；同一视觉动作不夸大真实能力；触摸端无悬停独占功能。

**风险**

- 当前获奖版本与当前活站可能不同。
- 历史内部工具和旧API不可直接当作新项目依赖。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
