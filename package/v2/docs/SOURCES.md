# 本轮官方参考来源

访问核验日期：2026-11-23。只总结与实现有关的规则，不复制受保护站点设计/图片。链接与核验结果另见 source-checks.json。

| 来源 | 用途与界限 |
|---|---|
| [W3C WCAG 2.2 Target Size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) | 目标尺寸含 24px 与间距/例外；本演示常规交互使用 44px，并不等于完整 WCAG 达标 |
| [GSAP matchMedia](https://gsap.com/docs/v3/GSAP/gsap.matchMedia/) | 媒体条件与动画清理，生命周期需测试 |
| [GSAP Standard License](https://gsap.com/standard-license/) | 许可允许用途、限制及版权；不是 MIT |
| [Three.js 源码与 MIT](https://github.com/mrdoob/three.js) | 本地 npm 0.187.0 的 geometry/material/renderer dispose API 与许可；旧 manual cleanup 链接本轮 404，不作为已读取的支持证据 |
| [Three.js docs](https://threejs.org/docs/) | API 参考；具体实现版本以本包锁定版本为准 |
| [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots) | 截图需要相同环境，基准差异不应以盲目更新消除 |
| [MDN reduced motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) | 根据用户减少动画偏好提供静态与暂停路径 |
| [U.S. Copyright Office](https://www.copyright.gov/what-is-copyright/) | 版权保护的基础说明；不代替逐资产许可核对 |

V1 历史来源位于 research 与原 docs，保留其不确定、冲突与日期口径；本轮没有把 206 个档案逐站重新研究或复刻。
