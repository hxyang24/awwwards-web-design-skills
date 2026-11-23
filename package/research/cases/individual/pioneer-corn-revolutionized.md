# Pioneer - Corn Revolutionized

- 案例 ID：`pioneer-corn-revolutionized`
- 奖项：2020-07，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/pioneer-corn-revolutionized

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2020-07。（s1: https://awwwards.com/resns-pioneer-corn-revolutionized-wins-site-of-the-month-july-2020.html）
- 官方说明Jelly为内部管线；使用GPU压缩纹理、按设备供给资源、MSDF文字和着色器混合烘焙光照。（s1: https://awwwards.com/resns-pioneer-corn-revolutionized-wins-site-of-the-month-july-2020.html）
- 以种子生命周期组织纵向故事，将育种和测试过程可视化。（s1: https://awwwards.com/resns-pioneer-corn-revolutionized-wins-site-of-the-month-july-2020.html）
- 该历史版本的制作方资料列出：Jelly。（s1: https://awwwards.com/resns-pioneer-corn-revolutionized-wins-site-of-the-month-july-2020.html）
- 该历史版本的制作方资料列出：Three.js。（s1: https://awwwards.com/resns-pioneer-corn-revolutionized-wins-site-of-the-month-july-2020.html）
- 该历史版本的制作方资料列出：GSAP。（s1: https://awwwards.com/resns-pioneer-corn-revolutionized-wins-site-of-the-month-july-2020.html）
- 该历史版本的制作方资料列出：Blender。（s1: https://awwwards.com/resns-pioneer-corn-revolutionized-wins-site-of-the-month-july-2020.html）
- 该历史版本的制作方资料列出：Octane。（s1: https://awwwards.com/resns-pioneer-corn-revolutionized-wins-site-of-the-month-july-2020.html）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 把科学流程拆成有独立标题和结论的章节。
2. 先用DOM图文解释各步骤，再决定哪些步骤必须用3D。
3. 把相机、动画和文字统一映射到章节进度。
4. 为WebGL中的重要标题提供语义HTML对应文本，避免重复朗读。

**移动/异常回退**：保留语义DOM内容和明确可点控件；触屏不依赖悬停，reduced-motion跳过视觉位移；按本例验收条目提供对应静态/列表入口。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 关闭动画仍能理解完整流程；每章可链接和定位；重要文本能搜索、复制并被辅助技术读取。

**风险**

- 当前获奖版本与当前活站可能不同。
- 历史内部工具和旧API不可直接当作新项目依赖。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
