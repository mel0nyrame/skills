# 仓库检查与评审

[English](maintaining.md) | 简体中文

## 检查

在仓库根目录使用 Python 3 运行：

```sh
python3 -B -m unittest discover -s tests -v
python3 -B skills/engineering/project-adr/scripts/check_adr.py docs/agents/adr
python3 -B -m scripts.check_docs
python3 -B -m scripts.check_pr_body --body-file /tmp/pr-body.md
```

[CI 工作流](../.github/workflows/tests.yml)在 Ubuntu 和 Windows 上运行回归、ADR 和文档检查。PR 事件还会检查正文。编辑 PR 标题或正文后，只重新检查正文结构，不重复运行完整矩阵。

文档检查器读取 Git 已跟踪和未被忽略的 Markdown，排除 `tests/fixtures/` 下的刻意构造输入。检查范围包括相对路径的行内链接、引用定义、Markdown 锚点、重复标题锚点和显式 HTML 锚点。

双语配对检查覆盖根目录的 `README.md` / `README.zh.md`，以及 `docs/` 下的所有 Markdown 文件。整个 `docs/agents/` 子树不参与配对检查。范围内每份文件必须有对应语言版本，并互相链接。

代码围栏中的示例、行内代码、注释和远程 URL 不参与链接验证。检查器支持本仓库常用的 Markdown 形式，不负责渲染全部扩展、访问远程链接或判断翻译是否准确。

PR 检查器要求按顺序提供 Summary、Evidence 和 Merge Danger。Summary 必须有视图；Evidence 必须有 Before/After；Door 必须为 one-way 或 two-way；Blast Radius 必须为一个词。评审者负责判断视图是否展示实际改动，以及证据是否支持结论。正文写法见 [PR 指南](engineering/pr.zh.md)。

## 评审

语义变化和工具输出规则见[评审标准](../CODING_STANDARDS.md)。检查主文件、条件参考、元数据和翻译之间的义务与条件。判断检查器行为与文档不一致前，先查阅已有测试。

完整 API 返回和命令日志保留在响应之外。提取当前判断需要的字段，失败时再展开。精简结果时保留被评审的提交和证据链接。

## 前向场景

按[场景流程](../tests/scenarios/README.md)从已提交版本创建独立项目。来源校验使用记录中的提交，支持历史版本。模型结果与输入准备、机械检查分别记录。
