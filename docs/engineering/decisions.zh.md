# Decisions 怎样保存工程选择及其理由

[English](decisions.md) | 简体中文 · [全部指南](../README.zh.md)

`decisions` 用来保存一项工程选择为什么成立，哪些方案已经比较过，以及什么条件变化后需要重新讨论。文件通常叫 ADR，即架构决策记录。这个 Skill 也处理架构之外的长期工程选择。

代码可以说明项目用了哪种数据库，却未必能解释为什么放弃另外两种。几年后重读一份合格的记录，应当能看懂当时的问题和取舍，而不必重新找回原来的聊天。

## 什么事情值得写一份记录

先遵守目标项目自己的创建条件。没有约定时，可以看这个问题以后是否容易被重新讨论，或忘记理由后是否容易再次选择一个已经证明不合适的方案。普通文字修正、局部样式调整，通常不需要新增 ADR。

本项目有一个现成例子。[第一份打包决策](../agents/adr/0001--categorized-plugin-layout.md)解释了为什么要让三个安装入口共用分类目录，以及为什么 Codex 保留兼容清单。[后续子模块决策](../agents/adr/0002--upstream-submodule-references.md)修改了其中的外部引用方式，同时保留其余打包选择。这样，读者可以分清哪些理由仍有效，哪些部分已经被替代。

## 怎样提出请求

在需要处理的项目中发送下面的请求。示例使用本项目的 Codex 插件。

```text
$skills:decisions
检查本项目关于上传文件保存位置的现有决策。
如果选择已经改变，写清新理由和真实备选方案，维护新旧记录的链接。
如果只是代码路径改变，同步原记录的事实。
先展示准备修改的文件，不归档或删除其他记录。
```

单独安装时使用 `$decisions`。Claude Code 插件中使用 `/skills:decisions`。如果你尚未作出选择，也可以要求整理 `proposed` 状态的提案，不能将仍在讨论的方案写成已经实施。

## 会生成什么文件

助手先找已有记录和项目模板。同一项决策已有负责人时，优先维护原文件。确实出现新的选择或替代关系时，才按项目制度新增记录。

项目完全没有约定时，一项决策放在一个 Markdown 文件中，默认路径如下。

```text
docs/adr/NNNN--kebab-title.md
```

例如 `docs/adr/0001--upload-storage.md` 是一个示例文件名，不会因为调用 Skill 就固定创建。归档的缺省位置是 `docs/adr/archive/`。本集合已经明确使用 `docs/agents/adr/`，因此维护本集合时沿用该目录。

默认英文记录采用下面的结构。这是结构示例，实际理由和备选方案需要来自真实调查。

```markdown
# Keep skill source in categorized directories

Status: implemented

## Problem
Readers need categories, while three installers need to find the same skills.

## Decision
Keep one source per skill and declare the paths each installer needs.

## Alternatives
A flat layout simplifies discovery but does not provide physical categories.

## Consequences and risks
Adding a category requires checking the installer paths and discovery results.
```

`proposed` 表示仍在考虑，`implemented` 表示已经实施，`rejected` 保存仍有预防价值的拒绝理由，`superseded` 表示被完全替代，`archived` 表示冻结的历史。项目已有状态体系时，继续遵守项目体系。

项目没有生命周期约定时，助手才读取[默认状态定义](../../skills/engineering/decisions/references/LIFECYCLE.md#default-states)。归档或删除记录前，再读取单独的[内容保留和依赖检查](../../skills/engineering/decisions/references/LIFECYCLE.md#archive-or-delete)。

## 实现变化后怎样维护

文件移动、配置键改名，但选择没变，就更新原记录中的事实。选择变了，就保留旧记录所代表的决定，并建立新旧关系。部分替代时，两份记录还可能各自负责一部分理由，不能为了整齐把旧内容全部删掉。

归档和删除需要符合任务授权。归档正文保持冻结。助手也不应为了填满模板编造备选方案；无法恢复的历史应写明缺口。

## 怎样验收

先读记录能否解释选择，再运行机械检查。检查器只验证默认结构、状态和本地链接路径，不会判断理由是否真实。

在本集合根目录，可以执行下面的命令检查本集合的记录。

```sh
python3 -B skills/engineering/decisions/scripts/check_adr.py docs/agents/adr
```

它会读文件并报告结果，不会替你生成 ADR。默认检查器也兼容完整的中文结构，但不能用它强行改造另一个项目的有效模板。详细约定见[执行指令](../../skills/engineering/decisions/SKILL.md)和[项目接入流程](../../skills/engineering/decisions/references/PROJECT-INTEGRATION.md)。
