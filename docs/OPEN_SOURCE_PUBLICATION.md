# 公开发布记录

公开仓库位于 https://github.com/hxyang24/awwwards-web-design-skills ，公开修订版本 v2.0.1。

源交付包 SHA-256：`5856a6ad5aae10765efda18e82383d2a738b3251733ff52ea40d614273baf8ee`。公开版的 ZIP、校验文件和冷启动回执另行生成，不能混用两个 ZIP 的哈希。

原完整包位于仓库 `package/`，保留 24 套技能、模板、研究和验证记录。旧版 187 个文件及技能脚本均保留原字节。为了公开发布，仅规范化这些 V2 元数据：

- `package/v2/contracts/v1-provenance.json`：省略私人聊天标识，保留原 ZIP 来源与摘要。
- `package/v2/evidence/cli-results.json`：Python 解释器绝对路径改为 `python`；实际退出码、断言结果和测试输出未改。
- `package/MANIFEST-V2.json`：针对公开版重新计算文件哈希。

仓库根目录新增 MIT、第三方声明、中文 README、贡献说明和锁定官方 action 提交的 Linux CI。package 内原有文档及版权说明继续保留。上述规范化不改变技能或演示的执行代码；公开版仍须通过原文件哈希与运行检查。

历史 Windows 测试、公开版解压启动和 GitHub CI 是独立证据，不将其中一个环境的通过推广到所有环境。可执行测试会改写 evidence，应在工作副本重跑。

## v2.0.1 在线验证修正

首次 Linux CI 的 57 个浏览器检查中，56 个通过；商品详情测试因列表页与详情页具有相同标题文字，等待条件可能提前满足。修正为等待 level=1 的详情主标题，再执行加购，不通过降低断言、移除检查或更改业务行为规避失败。在线初次运行记录： https://github.com/hxyang24/awwwards-web-design-skills/actions/runs/45126246184 。

公开版本的测试代码、package 版本、完整性清单及冷启动回执版本已同步更新；原始 V2.0 交付包未修改。后续 Linux 验证结果以对应提交的 Actions 为准。
