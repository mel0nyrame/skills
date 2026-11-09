# Skills

个人 Agent Skill 集合，覆盖工程流程、需求澄清、网络检索和知识沉淀。通过 Skills CLI 选择单项 Skill，或通过 Claude Code、Codex 安装完整插件。三个安装入口使用同一份源文件。

[English](README.md) | 简体中文

第一次使用时，从[中文使用指南](docs/README.zh.md)选择适合的 Skill，查看作用、示例和限制。

## 分类目录

### 工程流程

| Skill | 用途 |
| --- | --- |
| [project-engineering](docs/engineering/project-engineering.zh.md) | 实现项目改动，保存工程知识，同步受影响的决策。 |
| [project-adr](docs/engineering/project-adr.zh.md) | 保存长期设计讨论，维护选择、否决理由、生命周期和替代关系。 |
| [project-git](docs/engineering/project-git.zh.md) | 审查工作树、拆分提交，并按用户授权推送。 |
| [project-prose](docs/engineering/project-prose.zh.md) | 编写和审查自足的技术文字，保留完整契约。 |
| [pr ↗](https://github.com/mattpocock/skills/tree/main/skills/engineering/pr) | 外部推荐，指向 Matt Pocock 的上游 PR Skill。[使用指南](docs/engineering/pr.zh.md) · [子模块](skills/engineering/pr)。 |
| [retro ↗](https://github.com/mattpocock/skills/tree/main/skills/engineering/retro) | 外部推荐，指向 Matt Pocock 的上游复盘 Skill。[使用指南](docs/engineering/retro.zh.md) · [子模块](skills/engineering/retro)。 |
| [writing-for-agents ↗](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) | 外部推荐，指向 Matt Pocock 的上游 Agent 文档写作 Skill。[使用指南](docs/engineering/writing-for-agents.zh.md) · [子模块](skills/engineering/writing-for-agents)。 |

四个 `project-*` Skill 组成一套项目工程工具，分别负责实现与知识维护、长期决策、Git 交付和技术文字。每个 Skill 也可以单独使用。

### 思考与澄清

| Skill | 用途 |
| --- | --- |
| [clarify](docs/thinking/clarify.zh.md) | 检查假设；有关键缺口时只问一个问题，信息充分时直接回答。 |
| [karpathy-guidelines](docs/thinking/karpathy-guidelines.zh.md) | 保持任务范围，验证结果，清楚表达结论。内容来自个人维护的 fork。 |

### 检索工具

| Skill | 用途 |
| --- | --- |
| [firecrawl-mcp](docs/research/firecrawl-mcp.zh.md) | 通过 Firecrawl MCP 检索、核验、提取网页内容和执行浏览器交互。 |
| [tinyfish-mcp](docs/research/tinyfish-mcp.zh.md) | 通过 TinyFish MCP 执行网页自动化任务。 |
| [context7-mcp ↗](https://github.com/upstash/context7/tree/master/skills/context7-mcp) | 外部推荐，指向 Upstash 的官方 Context7 Skill。[使用指南](docs/research/context7-mcp.zh.md) · [子模块](skills/research/context7-mcp)。 |

### 知识沉淀

| Skill | 用途 |
| --- | --- |
| [recap](docs/knowledge/recap.zh.md) | 将会话整理为可复用、可追溯的专题知识。仅由用户显式调用。 |

项目包含 **9 个可安装 Skill**。`pr`、`retro`、`writing-for-agents` 和 `context7-mcp` 使用默认不检出的 Git 子模块，不进入插件和 Skills CLI 的 Skill 清单。对应使用指南提供精确的上游链接和单独安装方法。

## 安装

GitHub 安装命令要求先将此仓库发布到 `mel0nyrame/skills`。发布前使用本地安装方法。同一个 Agent 建议只选择一种安装方式，避免重复加载。

### Skills CLI

运行下面的命令，交互选择 Skill 和目标 Agent。

```sh
npx skills@latest add mel0nyrame/skills
```

可以安装单项 Skill，也可以只查看清单。

```sh
npx skills@latest add mel0nyrame/skills --skill clarify
npx skills@latest add mel0nyrame/skills --list
```

### Claude Code 插件

在 Claude Code 内执行下面的命令。

```text
/plugin marketplace add mel0nyrame/skills
/plugin install skills@mel0nyrame-skills
```

终端命令分别为 `claude plugin marketplace add mel0nyrame/skills` 和 `claude plugin install skills@mel0nyrame-skills`。安装后开启新会话。插件 Skill 使用 `skills` 命名空间，例如 `/skills:clarify`。

### Codex 插件

先添加 marketplace。

```sh
codex plugin marketplace add mel0nyrame/skills
```

打开 Codex，运行 `/plugins`，从 `mel0nyrame-skills` 安装 `skills`。如果当前 CLI 提供 `codex plugin add --help`，也可以直接安装。

```sh
codex plugin add skills@mel0nyrame-skills
```

直接安装命令已在 `codex-cli 0.166.0-alpha.5.1` 核实，其他版本的可用性取决于实际 CLI。安装后开启新会话。插件 Skill 使用 `skills` 命名空间，例如 `$skills:clarify`、`$skills:project-engineering`。通过 Skills CLI 单独安装时，使用 `$clarify`、`$project-engineering`。

### 本地安装

在仓库根目录执行。每种安装方式都会写入目标 Agent 的正常配置。

```sh
# Skills CLI：先查看清单，再选择 Skill 和目标 Agent。
npx skills@latest add . --list
npx skills@latest add .

# Claude Code：添加本地仓库，再安装插件。
claude plugin marketplace add .
claude plugin install skills@mel0nyrame-skills

# Codex：添加本地仓库，再通过 /plugins 或可用的 CLI 安装。
codex plugin marketplace add .
codex plugin add skills@mel0nyrame-skills
```

## 行为与依赖

- `clarify` 在仍有关键缺口时只问一个问题并等待回复。已有上下文充分时，它在同一轮直接回答。
- `recap` 仅由用户显式调用。保留 `disable-model-invocation: true` 和 Codex 禁止隐式调用的设置。
- `project-git` 分别检查 commit、push 和 PR/MR 操作的授权。先检查项目规则和稳定的结构化提交历史，再决定是否使用中文默认说明。用户对本次任务的明确要求优先。
- `project-adr` 优先遵守目标项目约定。默认检查器接受完整的英文或中文结构，并保留归档排除规则。
- `project-engineering` 和 `project-git` 的 PR/MR 正文编写依赖单独安装的上游 `pr`。依赖缺失时报告缺口，不静默安装。
- Firecrawl 和 TinyFish Skill 需要分别配置对应 MCP 服务。项目仅提供 Skill 和依赖元数据，不包含服务配置或凭据。

## 维护

### 发布与版本

`main` 用作发布分支，日常开发放在功能分支。发布 PR 同步修改两份插件清单的版本，合并后再在对应的 `main` 提交上创建 `vX.Y.Z` 标签。一个标签代表整个集合，单项 Skill 不单独编号。例如，`v0.1.0` 对应两份插件清单中的 `version: "0.1.0"`。

`skills@latest` 选择安装工具的版本。默认安装命令读取本仓库的默认分支，不会自动选择最新 Git 标签。需要固定一个已经发布的历史版本时，明确指定标签来源。

```sh
npx skills@latest add https://github.com/mel0nyrame/skills/tree/v0.1.0
```

已发布标签保持不动。已有安装需要另行运行 `npx skills@latest check` 和 `npx skills@latest update`。调整发布方式前，先阅读[版本决策](docs/agents/adr/0003--repository-release-versions.md)。

### 仓库维护

上游子模块设置 `update = none`，正常初始化时不检出内容。`git submodule status` 中开头的 `-` 是预期状态。显式检出这些目录可能让递归扫描发现上游的其他 Skill。需要使用指定 Skill 时，按指南单独安装。[子模块决策](docs/agents/adr/0002--upstream-submodule-references.md) 说明了这个边界。

Skill 指令使用英文。同步维护本文件与 [README.md](README.md)。每个 Skill 只有一个源目录。改名时同步修改 frontmatter、展示信息、默认提示词和相互引用。新增分类时，也要更新 Claude 的 Skill 路径。

面向使用者的指南位于 `docs/<类别>/<skill>.md`，并配套 `<skill>.zh.md`。两个语言版本与对应 `SKILL.md` 保持一致，用来解释用法，不另行定义执行流程。项目自身的 ADR 位于 `docs/agents/adr/`。

替换 Codex 兼容清单前，先验证新格式能发现分类目录中的 Skill。[打包决策](docs/agents/adr/0001--categorized-plugin-layout.md) 说明发现机制和备选方案。决策或依据变化时同步更新记录。引入第三方内容时保留来源和许可通知。根 `LICENSE` 是自有内容许可的权威文本；同步维护对应 Skill 目录中的副本，使单独安装也携带许可通知。Karpathy 的许可和来源通知由其自身目录保存。

在仓库根目录运行下面的检查。

```sh
python3 -B -m unittest discover -s tests -v
python3 -B skills/engineering/project-adr/scripts/check_adr.py docs/agents/adr
npx skills@latest add . --list
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

修改打包方式后，还需在隔离的 Claude/Codex 安装环境中核对实际 Skill 清单。清单格式有效不能证明 9 个 Skill 都能加载。GitHub 远程安装需要发布仓库后单独验证。

安装格式依据包括 [Skills CLI](https://github.com/vercel-labs/skills)、[Claude 插件文档](https://code.claude.com/docs/en/plugins) 和 [Codex 插件打包文档](https://developers.openai.com/plugins/build/plugins)。

## 许可与来源

mel0nyrame 的自有内容采用 MIT。项目中的 Karpathy fork 保留上游 MIT 声明和来源。外部推荐遵循各自的上游许可。详见 [LICENSE](LICENSE)、[第三方通知](THIRD_PARTY_NOTICES.md) 和 [Karpathy 许可条款](skills/thinking/karpathy-guidelines/LICENSE)。
