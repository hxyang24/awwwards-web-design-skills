# Awwwards Research & Reusable Skills — 全套交付包

**交付内容：206 条官方来源作品档案、30 个技术拆解案例、12 个 SKILL.md 技能、六套原创可运行网站蓝本、配套脚本、验收流程与完整研究报告。**

> 数据基准：2026-11-23。为保证诚实交付：206 条是收集到的记录数，不代表历史每个月份均完成核验。原始技能目录不可访问，本包中的技能脚本为依据上一轮报告重建的可运行版本，并非其原始源文件逐字节压缩。

## 建议从这里开始

打开 **`AGENT_START_HERE.md`**。它是给 AI 代理的完整执行步骤，能在缺少现场上下文时提供保守安全的默认逻辑。

## 压缩包目录

```text
Awwwards_Research_Skills_Full/
├── README.md                    # 本页
├── AGENT_START_HERE.md          # AI 完整流程入口
├── INSTALL.sh                   # 安装到自定义本地 skills 目录，不覆盖已有目录
├── research/
│   ├── Awwwards_Research_Skills_2026-11-23.html
│   ├── archive/sites_of_the_month.{json,csv}
│   ├── archive/timeline.csv
│   ├── archive/by_year/        # 18 份逐年索引
│   ├── cases/representative_30.{json,csv}
│   ├── cases/individual/       # 30 份单案例拆解
│   └── coverage/               # 证据缺口、数据字典及上轮声明
├── skills/                      # 12 个 SKILL.md + scripts / references / templates
├── examples/                    # 6 套完整生成的网站
├── tests/                       # 实际检查结果与测试脚本
└── docs/                        # 证据、版权与重建说明
```

## 安装到任意 AI 开发环境

在解压后包根目录运行：

```bash
# 使用你想安装的本地 skill 文件夹，不要传入项目文件根目录。
bash INSTALL.sh --target "$HOME/.agents/skills"
# 其他兼容 SKILL.md 的 AI 环境，可以选择对应的目录，例如 ~/.claude/skills
```

此脚本只复制不存在的 `awwwards-*` 技能；已存在目录会跳过。它不会登录你的服务端，不会修改 GitHub 项目，不会自动部署。某些平台不支持从文件系统读取 Skills，此时把对应 SKILL.md 和关联文件交给 AI，按 `AGENT_START_HERE.md` 执行。

## 直接运行六类示例

| 示例目录 | 能做什么 | 明确不能做什么 |
|---|---|---|
| `examples/saas/` | 响应式官网和本地表单验证 | 不发送预约请求 |
| `examples/commerce/` | 商品筛选和对话框预览 | 不下单、不支付 |
| `examples/dashboard/` | KPI 和表格本地搜索 | 不读取真实账户 |
| `examples/portfolio/` | 项目卡片和导航 | 不代表真实项目资料 |
| `examples/editorial/` | 目录、文章、阅读进度 | 不假定原站代码 |
| `examples/immersive/` | 场景感构图及章节导航 | 没有真实 3D 渲染 |

```bash
cd examples/saas
python -m http.server 8000
# 浏览器中访问 http://localhost:8000
```

这些原创网页蓝本没有外部 CDN 依赖，静态阅读不会依赖 JS。浏览器行为、视觉表现和性能预算仍需在真实浏览器中另行验证。

## 数据查询与完整性核验

```bash
python skills/awwwards-research/scripts/archive_tool.py stats
python skills/awwwards-research/scripts/archive_tool.py search --year 2025
python skills/awwwards-research/scripts/archive_tool.py missing
python skills/awwwards-reference/scripts/case_tool.py list
python skills/awwwards-reference/scripts/case_tool.py validate
python tests/run_all.py
python skills/awwwards-release/scripts/delivery_manifest.py --verify MANIFEST.json --root .
```

其他文档见 `docs/RECONSTRUCTION_NOTES.md` 与 `docs/RIGHTS_AND_SOURCES.md`。

## 本次重新打包的真实验证结果

- `tests/package-test-results.json`：**42/42 CLI、数据、合同与负例检查通过**。
- `tests/offline-dom-results.json`：**12/12 Chromium DOM、响应式和交互检查通过**（每类 390px 和 1440px 视宽各一组）。
- `tests/screenshots/`：12 张该离线渲染方法下的截图。
- 该离线浏览器检查通过 `page.set_content()` 注入本地 CSS 和转换后的 JS；它**没有测试 HTTP 导航、原生模块网络加载、部署兼容性或 Core Web Vitals**。
- 研究网站本身没有在这次打包中重新进行实时浏览器检查；研究来源边界请看 `research/README.md`。

运行 `python skills/awwwards-release/scripts/delivery_manifest.py --verify MANIFEST.json --root .` 可校验本包文件的 SHA-256 完整性。
