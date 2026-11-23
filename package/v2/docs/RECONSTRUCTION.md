# 授权参照 → 原创重建 → 差异评估

输入 `reference-brief.example.json` 的结构，补齐来源与授权，不能将一张截图解释为完整产品。只有桌面截图时，移动布局是推断，需要明确标记。

在 v2 目录运行（先 npm ci 安装测试工具）：
```text
node tools/capture.mjs http://127.0.0.1:4173/v2/demos/reference/ evidence/reference.png 1440 1000
node tools/inspect_image.mjs evidence/reference.png evidence/reference-analysis.json
node tools/capture.mjs http://127.0.0.1:4173/v2/demos/enterprise/ evidence/candidate.png 1440 1000
node tools/visual_diff.mjs evidence/reference.png evidence/candidate.png evidence/comparison contracts/visual-config.example.json
python tools/validate_contract.py reference contracts/reference-brief.example.json
```
上例 candidate 是另一种页面，因此差异预期失败，用于说明工具不会把任意页面判为复现成功。真正重建时 candidate 应指向相应实现。

`capture` 默认只允许 localhost/127.0.0.1/[::1]；若用户明确授权观察公开或自己的远程站点，可使用 `--allow-remote`。禁止绕过登录、验证码、付费限制；截图可能包含个人信息，不要未经授权打包传播。

差异输出包含尺寸、未遮罩像素数、changed ratio、平均通道差、区域报告、diff PNG。阈值默认 ratio 0.005、pixel_threshold 0.1，仅是示范，按项目批准基准调整。mask 必须有 reason，配置和报告保留遮罩信息；不得遮蔽关键 CTA/金额等以掩盖缺陷。

不进行自动字体身份识别、OCR、语义页面生成或无限自动修正。inspect_image 只计算 PNG 尺寸与量化主色，布局和交互来自人工/AI 观察并需要浏览器复核。

## 已实测的独立重建简例
`demos/reference/` 是本包原创授权目标；`demos/reconstruction/` 使用独立 HTML 与 CSS 重建其结构、字体层级和主操作，不导入目标页面样式表。浏览器分别在 390 与 1440 宽度截图并检查全图及标题/操作区域阈值，证据位于 `evidence/reconstruction-*.json/png`。这只证明一个受控原创页面的重建和比较流程可运行，不代表任意第三方网站的逐页复现。
