# Writing-for-agents 怎样写面向 Agent 的文档

[English](writing-for-agents.md) | 简体中文 · [全部指南](../README.zh.md)

这是 [Matt Pocock 上游 writing-for-agents Skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) 的使用说明。它用于编写面向 Agent 的文档：Skill、`AGENTS.md`、`CLAUDE.md` 等指令文件。它强调上下文指引、信息层级、明确的完成条件和删减，而不是堆长篇说明。

上游目录位于 `skills/productivity/`。本集合把[子模块](../../skills/engineering/writing-for-agents)放在 `skills/engineering/`，避免新增分类。本页链接指向上游的真实目录。

## 先安装

它属于外部 Skill，不包含在本集合安装的 9 个 Skill 中。可以单独安装。

```sh
npx skills@latest add mattpocock/skills --skill writing-for-agents
```

选择目标 Agent，并按上游说明确定调用名称。子模块只记录固定提交的上游仓库，正常情况下不检出内容，不代表安装完成。用它编写 Skill 时，上游 Skill 会读取自己的 `SKILL-MECHANICS.md` 取得详细规则。

## 怎样提出文档修改请求

```text
$writing-for-agents
重写这个 Skill 的 SKILL.md 中的完成条件。
保留现有适用范围和调用策略，把含糊的指令换成可观察的检查项，
删除重复的限制说明，并报告删了什么。不要发布、commit 或 push。
```

这是教学示例。实际请求要写明文件、目标行为，以及哪些内容必须保留。

## 最后得到什么，会不会生成文件

上面的请求通常得到修改后的文档，或只读审查意见，取决于你的要求。没有指定保存位置时，一般不生成文件。这个 Skill 提供写作规则，不负责安装服务、运行项目测试，也不授权 Git 交付。

[retro](retro.zh.md) 会调用这个 Skill 取得写作风格指南。准备使用 retro 时，两者都要安装。

## 怎样验收

检查每条指令是否写清动作、对象和完成条件。确认必要的限制、例外和调用策略仍在。删减后丢掉条件的文档，即使更短也不算合格。

上游完整指令和署名见[原文](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md)及[第三方通知](../../THIRD_PARTY_NOTICES.md)，本页不保存其指令副本。
