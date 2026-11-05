# Firecrawl MCP 怎样把网页信息整理成可核对的结果

[English](firecrawl-mcp.md) | 简体中文 · [全部指南](../README.zh.md)

`firecrawl-mcp` 指导助手使用已连接的 Firecrawl 工具。它可以帮助寻找网页、读取已知链接、提取字段，也可以在确实需要时操作动态页面或收集一个限定范围内的站点内容。

你指定 Firecrawl，或助手已为任务选择 Firecrawl MCP 工具时，使用这个 Skill。明确指定其他服务时，保留该选择。执行 Map、Crawl 或 Agent 操作前，助手会分别读取 URL 发现、多页收集或研究任务子章节。

如果你想把几个网页里的信息整理成同一种格式，这个 Skill 会影响工具选择、结果核对和来源保留。安装 Skill 只增加使用指令，Firecrawl MCP 服务还需要在 Agent 中单独连接。

## 先确认能不能调用服务

MCP 是助手访问外部工具的一种连接方式。进入会话后，相关 Firecrawl 工具必须实际可见。工具不可用时，助手应报告连接或会话加载的问题，不能把另一项服务的结果说成 Firecrawl 已成功返回。

本集合的安装不会提供服务凭据。认证、额度和可用工具由你的连接决定。先从一两个已知页面开始，比分配一个没有范围的整站抓取任务更容易确认结果。

如果你的 Agent 支持 HTTP MCP 连接，可以从它的 MCP 服务设置进入配置。本 Skill 的[连接元数据](../../skills/research/firecrawl-mcp/agents/openai.yaml)声明的服务地址如下。它是工具服务地址，需要提取内容的网页 URL 另行提供。完成服务要求的认证后，回到会话检查工具是否可见。

```text
https://mcp.firecrawl.dev/v2/mcp
```

## 用一项有明确产物的任务开始

下面的请求用价格页提取作教学示例。它没有给出真实价格，也不承诺任何服务费用。

```text
$skills:firecrawl-mcp
读取我接下来提供的两个官方价格页。
提取方案名称、价格、币种、计费周期和来源 URL。
将结果保存到 data/pricing.csv，并在对话中说明缺失字段和读取失败的页面。
不要猜测未公开价格，不提交表单，不创建持续监控。
```

示例使用本项目的 Codex 插件。单独安装时用 `$firecrawl-mcp`，Claude Code 中用 `/skills:firecrawl-mcp`。把需要读取的真实 URL 一并提供给助手。如果只想看表格，就将保存文件那句换成“只在对话中返回表格”。

## 助手会怎样处理这些页面

已有 URL 时，优先直接阅读页面。需要先找来源时才检索。阅读结果不包含必要字段时，应检查原页面；确实需要点击或动态加载时，再考虑交互。

你要求收集一个站点时，还需要约定路径、页数和深度。长任务可能先返回任务编号，助手要保留编号并继续检查状态。拿到编号不代表内容已经收集完成。

调用 Search 前，助手先读[检索请求](../../skills/research/firecrawl-mcp/references/workflows.md#search-requests)。页面问答和指定字段提取先读[定向提取](../../skills/research/firecrawl-mcp/references/workflows.md#targeted-extraction)。普通 Markdown 页面读取直接使用主文件中的规则，无需加载这些示例。

浏览器交互、本地文件上传、付费数据操作等条件任务开始前，助手会按照[操作对应的读取入口](../../skills/research/firecrawl-mcp/SKILL.md#read-before-conditional-operations)加载所需规则。每个入口只加载对应流程。

提取到数字之后，还要确认它对应哪个方案、币种和计费周期。自动摘要或问答结果仍需对照来源核验，不能直接当作逐字引文。

## 文件究竟从哪里来

`data/pricing.csv` 来自上面请求中明确指定的保存动作。Firecrawl 返回内容后，助手还需要本地文件写入能力才能把它保存到这个位置。服务返回成功本身不会保证你的项目里出现 CSV。

文件的字段可以按下面的表头组织，实际行内容来自读取结果。

```csv
plan,price,currency,billing_period,source_url
```

| 请求方式 | 主要产物 |
| --- | --- |
| 只让助手阅读或比较网页 | 对话中的答案、表格和来源链接，没有固定本地文件 |
| 明确要求保存 CSV、JSON 或 Markdown | 你指定路径中的文件，以及实际保存结果 |
| 启动异步收集任务 | 服务侧任务编号，随后才有成功、失败和结果内容 |

截图、下载文件或服务端文件地址也不自动等于本地文件路径。需要落地时，应报告文件实际保存在哪里。

## 怎样验收，以及哪些情况需要停下来

打开保存的 CSV，检查每行是否有可访问的来源，计费周期是否保留，缺失值有没有被编造成数字。再抽查几个关键字段，与页面当前内容对照。缓存内容可能晚于页面更新，实时性要求应在请求中说明。

认证失败、额度不足或服务报错时，应报告实际失败范围。不要因为页面没读全，就交付一份看似完整的比较表。提交表单、执行付费数据操作和创建持续监控，还需要相应授权。

工具选择和结果检查以[执行指令](../../skills/research/firecrawl-mcp/SKILL.md)为准，长任务和文件等细节见[按需流程](../../skills/research/firecrawl-mcp/references/workflows.md)。已有 TinyFish 连接时，也可以阅读 [TinyFish 指南](tinyfish-mcp.zh.md)，按实际工具选择服务。
