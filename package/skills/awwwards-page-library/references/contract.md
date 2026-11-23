# 页面模式与业务路由 执行契约

## 最小输出
输出 route-map.json（path、pattern_id、goal、permission、states、evidence），以及主路径和剩余规格清单。

## 不变量
先识别用户要完成的任务，再组合页面；不要把营销首页直接套进交易或后台。目录的 specification 记录只是规格，runnable_demo 才有演示路由。

## 主路径与失败路径
执行前记录任务入口、权限、数据前置条件；操作后核对实际状态、返回路径和用户反馈。测试不能只检查按钮存在。
- `marketing.home`：建立品牌定位并进入核心服务。约束：不得虚构客户或转化数字。
- `marketing.about`：理解团队与公司背景。约束：人物与资质需要真实来源。
- `marketing.solutions`：按问题选择方案。约束：区分已上线能力与规划。
- `marketing.pricing`：比较价格并理解计费规则。约束：总价、税费、自动续费应透明。
- `marketing.contact`：提交可追踪的联系请求。约束：无服务端只能标为本地预览。
- `marketing.case-study`：了解客户问题和成果证据。约束：收益数据必须有可引用证据。
- `marketing.careers`：找到适合的职位。约束：不虚构开放岗位。
- `marketing.campaign`：理解活动并完成报名。约束：明确时区与报名是否真实生效。
- `marketing.comparison`：比较适用场景和功能。约束：竞品主张必须有日期与来源。
- `marketing.portfolio`：快速理解创作能力。约束：标明个人贡献与素材许可。
- `auth.login`：安全进入已有账户。约束：登录成功应来自真实会话。
- `auth.signup`：建立账户并理解条款。约束：不要预勾选营销同意。
- `auth.reset-password`：恢复访问。约束：避免泄漏账户是否存在。
- `auth.mfa`：完成额外验证。约束：限制重试与验证码暴力破解。
- `auth.invite`：确认加入组织及角色。约束：拒绝过期或不匹配邀请。
- `auth.access-denied`：理解缺少的权限。约束：不泄漏受保护资源详情。
- `content.article-list`：找到需要阅读的内容。约束：区分广告与编辑内容。
- `content.article`：持续阅读并理解出处。约束：署名和转载许可明确。
- `content.search`：找到匹配资料。约束：空结果提供修正方式。
- `content.docs`：完成具体使用任务。约束：文档应对应真实版本。
- `content.video`：按偏好观看或阅读内容。约束：不自动播放有声媒体。
- `content.immersive`：在不丢失内容的情况下探索。约束：WebGL 不能阻断核心内容。
- `community.feed`：浏览与相关互动。约束：无限滚动保留可访问分页。
- `community.profile`：理解用户公开身份。约束：公开字段与私有字段分离。
- `community.discussion`：参与有上下文的讨论。约束：处理用户输入的脚本注入。
- `community.messages`：安全交流并管理会话。约束：明确发送成功与本地排队。
- `community.notifications`：处理需要关注的事件。约束：不凭展示状态断言外部工作完成。
- `education.courses`：选择适合的课程。约束：课程效果主张需要依据。
- `education.lesson`：持续完成学习单元。约束：进度持久化边界明确。
- `education.assessment`：理解并提交答题结果。约束：支持键盘并避免仅颜色反馈。
- `education.progress`：理解已学内容和下一步。约束：不从停留时长推断学习效果。
- `education.certificate`：核验证书的颁发依据。约束：不得伪造资格或认证。
- `booking.availability`：找到可用时间。约束：确认前重新校验可用性。
- `booking.booking`：审阅并确认预约信息。约束：演示不能假装占用真实时段。
- `booking.itinerary`：了解已预约安排。约束：外部变更需明确授权。
- `booking.service-detail`：理解服务内容和适用范围。约束：不虚构专业资质。
- `system.loading`：理解等待中的任务。约束：避免布局跳动和无结束等待。
- `system.empty`：理解原因并开始行动。约束：区分无数据和无权限。
- `system.error`：修复失败并保留输入。约束：不重复提交已执行的副作用。
- `system.not-found`：重新找到目的地。约束：不泄漏内部路由或堆栈。
- `system.maintenance`：理解服务可用性。约束：预计恢复时间必须有来源。
- `system.consent`：理解并控制可选数据使用。约束：不将可选追踪默认为必需。

## 证据结构
```json
{"id":"page-patterns-primary-flow","status":"not_run","method":"browser interaction or focused unit test","environment":null,"evidence":[],"limitations":[]}
```
只有执行后填写 `passed` 或 `failed`；无法运行记 `blocked` 并说明条件。参考来源见完整包 `v2/docs/SOURCES.md`，可用规范入口：W3C WCAG 2.2、MDN prefers-reduced-motion、GSAP 官方文档、Three.js 官方文档、Playwright 官方文档。

## 移植与维护
已有 React/Vue/Next/Nuxt 项目优先复用其路由、组件和数据层；原生 HTML 示例仅为行为参照。不得声称示例已通过这些框架的构建测试。业务接口、密钥管理、服务端授权、数据持久化与生产部署需要项目实际接入和验证。
