# 公开发布记录

公开仓库位于 https://github.com/hxyang24/awwwards-web-design-skills ，代码版本 v2.0.0。

源交付包 SHA-256：`5856a6ad5aae10765efda18e82383d2a738b3251733ff52ea40d614273baf8ee`。公开版的 ZIP、校验文件和冷启动回执另行生成，不能混用两个 ZIP 的哈希。

原完整包位于仓库 `package/`，保留 24 套技能、模板、研究和验证记录。旧版 187 个文件及技能脚本均保留原字节。为了公开发布，仅规范化这些 V2 元数据：

- `package/v2/contracts/v1-provenance.json`：省略私人聊天标识，保留原 ZIP 来源与摘要。
- `package/v2/evidence/cli-results.json`：Python 解释器绝对路径改为 `python`；实际退出码、断言结果和测试输出未改。
- `package/MANIFEST-V2.json`：针对公开版重新计算文件哈希。

仓库根目录新增 MIT、第三方声明、中文 README、贡献说明和锁定官方 action 提交的 Linux CI。package 内原有文档及版权说明继续保留。上述规范化不改变技能或演示的执行代码；公开版仍须通过原文件哈希与运行检查。

历史 Windows 测试、公开版解压启动和 GitHub CI 是独立证据，不将其中一个环境的通过推广到所有环境。可执行测试会改写 evidence，应在工作副本重跑。
