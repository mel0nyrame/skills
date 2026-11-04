# 从任务和产物选择 Skill

[English](README.md) | 简体中文 · [安装方法](../README.zh.md#安装)

这个集合里的 Skill 会指导 AI 助手怎样处理任务。你提出同一个请求，助手应当按相应规则调查、执行和检查结果。安装 Skill 只是让这些指令可被调用，外部服务连接和文件操作权限仍由你的 Agent 环境提供。

先想清楚你要得到什么。要一轮澄清对话，可以用 `clarify`。要修改项目并留下后续能用的工程知识，可以从 `project-engineering` 开始。要把会话整理成独立专题，再用 `recap`。它们的文件产物和操作范围差别很大。

## 每个 Skill 具体做什么，会留下什么

| Skill 和详细指南 | 适合交给它的任务 | 通常能得到什么 |
| --- | --- | --- |
| [clarify](thinking/clarify.zh.md) | 先明确真正要解决的问题 | 对话中的关键问题及后续方案，没有默认文件 |
| [karpathy-guidelines](thinking/karpathy-guidelines.zh.md) | 控制工作范围，核实假设和结果 | 原任务的代码、文档或答案，没有固定产物目录 |
| [project-engineering](engineering/project-engineering.zh.md) | 按项目规则实现功能、修复或迁移 | 相关源文件和测试，必要时更新工程知识及决策 |
| [project-adr](engineering/project-adr.zh.md) | 保存长期提案与选择，接续议题并维护记录 | 项目 ADR 目录中的议题记录，包含否决理由、未决问题、状态和链接 |
| [project-git](engineering/project-git.zh.md) | 审查改动、拆分提交、按授权推送 | 审查说明、本地提交哈希或推送结果，取决于授权 |
| [project-prose](engineering/project-prose.zh.md) | 让技术说明脱离聊天也能读懂 | 指定文档或注释的更新，或只读审查意见 |
| [pr](engineering/pr.zh.md) | 根据真实 diff 和验证结果写 PR 正文 | 对话草稿，或你指定的 `PR.md` 等文件 |
| [firecrawl-mcp](research/firecrawl-mcp.zh.md) | 读取和提取网页内容 | 有来源的答案、结构化结果，明确要求后再保存文件 |
| [tinyfish-mcp](research/tinyfish-mcp.zh.md) | 读取网页，必要时执行筛选和点击 | 提取数据、任务状态，明确要求后再保存文件 |
| [context7-mcp](research/context7-mcp.zh.md) | 查阅匹配版本的开发文档 | 文档依据、代码示例和解释，查询本身不改项目 |
| [recap](knowledge/recap.zh.md) | 从会话保存或查询可复用知识 | 独立知识库中的专题、来源、导读及变更记录 |

上表描述常见结果，不代表每次都固定创建这些文件。单篇指南会说明实际路径、出现条件，以及怎样检查结果。

## 安装后怎样开始一次任务

先按页首的安装方法完成安装，再选择指南中的调用示例。下面三种名称表示同一个内置 Skill，取决于安装方式。

| 安装方式 | 调用示例 |
| --- | --- |
| Codex 单独安装的 Skill | `$clarify` |
| 本集合的 Codex 插件 | `$skills:clarify` |
| 本集合的 Claude Code 插件 | `/skills:clarify` |

名称后面跟上任务、输入材料和操作范围。示例中的路径需要换成你自己的项目路径。代码块只是请求示例，阅读页面不会执行它。

```text
$skills:project-engineering
给当前项目增加 CSV 导出，复用已有权限检查。
先确认修改入口，完成实现后运行相关检查。
报告改了哪些文件、保存了哪些有长期价值的知识。
不要暂存、commit 或 push。
```

这段请求允许实现和验证，同时保留 Git 交付边界。如果只想先了解方案，应把范围改成只读调查。

## 从一项功能到交付，怎样组合才有意义

以导出功能这个教学示例来说，`project-engineering` 先确认项目规则和实现入口，再修改功能及测试。有值得长期保留的发现时，它优先补进已有工程文档。目标项目没有合适负责人时，才考虑 `docs/engineering/ENGINEERING.md` 或 `DATA.md` 这些缺省位置。

设计议题具有长期价值时，`project-adr` 就在讨论中保存理由、已评估方案、未决问题和替代关系，尚未选定或实施时也可以记录。`project-engineering` 在选择方案前读取相关记录，并随实现变化同步。目标项目没有约定时，默认记录放在 `docs/adr/`。本集合自己的记录使用 `docs/agents/adr/`，不会因此要求所有项目使用同一路径。

代码和说明准备好以后，你可以让 `project-git` 先审查，再明确决定是否 commit 或 push。需要评审正文时再调用外部 `pr`。一次小改动不需要把所有 Skill 依次运行一遍。

## 外部服务和知识库有什么额外条件

Firecrawl 和 TinyFish 指南依赖相应 MCP 连接。MCP 是 Agent 调用外部工具的连接方式，安装文字指令不能替代连接。读取结果默认可以留在对话里。要求 CSV 或 JSON 时，要明确保存路径，助手也需要能写入本地文件。

Context7 和 PR 来自外部项目，需要单独安装，具体命令在各自指南中。本集合有 9 个内置 Skill，两个子模块只是上游引用。它们设置 `update = none`，正常情况下不检出上游完整内容。在 GitHub 上点击子模块会打开上游仓库的固定提交，指南保留直达具体 Skill 子目录的链接。

`recap` 操作独立知识库。它的初始化、候选检查和正式发布可能创建 Git 提交。只想先看内容时，应明确要求未提交草稿。查询正式知识也可能更新缓存或锁文件，严格只读任务需要先核对访问方式。

## 怎样检查助手交付的东西

拿到文件路径后实际打开，确认内容存在，来源能访问。拿到测试结论时，核对执行命令和结果。拿到服务任务编号时，继续检查是否完成，不能把编号当成最终数据。

各篇指南都写明了产物和验收方法。Agent 执行的详细规则由对应 `SKILL.md` 负责；这些使用指南解释怎样提出请求和判断结果。本集合的维护理由保存在[项目 ADR](agents/adr/)，不要求普通使用者先读完整套工程决策。
