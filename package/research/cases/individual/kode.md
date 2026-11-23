# Kode Sports Club

- 案例 ID：`kode`
- 奖项：2020-11，状态：`primary_month_claim`
- 研究级别：`desk_researched`
- 官方页面：https://www.awwwards.com/sites/kode

## 有来源的公开事实

- 官方来源记录该案例的SOTM月份为2020-11。（s1: https://awwwards.com/kode-sports-club-by-merci-michel-wins-site-of-the-month-november-2020.html）
- 官方记录了导出时复用重复物体、合并网格、纹理通道着色、简化网格求高度与分区减少射线测试等取舍。（s1: https://awwwards.com/kode-sports-club-by-merci-michel-wins-site-of-the-month-november-2020.html）
- 俯视地图与第三人称角色参观之间连续切换，加入场所介绍和成就。（s1: https://awwwards.com/kode-sports-club-by-merci-michel-wins-site-of-the-month-november-2020.html）
- 该历史版本的制作方资料列出：Three.js。（s1: https://awwwards.com/kode-sports-club-by-merci-michel-wins-site-of-the-month-november-2020.html）
- 该历史版本的制作方资料列出：WebGL。（s1: https://awwwards.com/kode-sports-club-by-merci-michel-wins-site-of-the-month-november-2020.html）
- 该历史版本的制作方资料列出：Blender Python API。（s1: https://awwwards.com/kode-sports-club-by-merci-michel-wins-site-of-the-month-november-2020.html）
- 该历史版本的制作方资料列出：Draco。（s1: https://awwwards.com/kode-sports-club-by-merci-michel-wins-site-of-the-month-november-2020.html）
- 该历史版本的制作方资料列出：glTF。（s1: https://awwwards.com/kode-sports-club-by-merci-michel-wins-site-of-the-month-november-2020.html）

## 原创实现蓝图

### 复用机制的原创实现蓝图

**输入**：经过核验的自有正文与主用户任务；已授权图片/视频/模型；用户操作与设备能力

**状态**：idle → loading → ready → interacting → paused → error → fallback → disposed

**实施步骤**

1. 将设施列表作为主信息，3D作为探索入口。
2. 为重复模型保存变换数据，比较实例化和合并后的实际draw calls。
3. 指针落点先与平面求交，再用简化导航网格计算高度。
4. 保留“回到地图”“跳到设施”和触摸替代控制。

**移动/异常回退**：保留语义DOM内容和明确可点控件；触屏不依赖悬停，reduced-motion跳过视觉位移；按本例验收条目提供对应静态/列表入口。

**资源清理**：卸载时停止本模块动画帧、断开观察器、移除事件监听；若存在GPU/音频/视频资源则分别释放或停止；不得全局销毁其他页面资源。

**验收条件**

- [ ] 用户被障碍卡住能重置；设施列表直接可达；缩放和旋转不阻断正文阅读。

**风险**

- 当前获奖版本与当前活站可能不同。
- 历史内部工具和旧API不可直接当作新项目依赖。

## 当前证据边界

> 本次为文献研究，未进行该站的实时浏览器交互或独立性能测量。蓝图属于原创实现建议。
