# Project ADR 怎样保存工程选择及其理由

[English](project-adr.md) | 简体中文 · [全部指南](../README.zh.md)

`project-adr` 在设计讨论中保存有长期价值的提案、已选方案、否决理由和未决问题，让下一个 agent 能接续工作。它也维护实现事实和替代关系。文件通常叫 ADR，即架构决策记录。记录范围也包括架构之外的长期工程选择。

代码可以说明项目用了哪种数据库，却未必能解释为什么放弃另外两种。几年后重读一份合格的记录，应当能看懂当时的问题和取舍，而不必重新找回原来的聊天。

## 什么事情值得写一份记录

先遵守目标项目自己的创建条件。没有约定时，可以看这个问题以后是否容易被重新讨论，或忘记理由后是否容易再次选择一个已经证明不合适的方案。普通文字修正、局部样式调整，通常不需要新增 ADR。

本项目有一个现成例子。[第一份打包决策](../agents/adr/0001--categorized-plugin-layout.md)解释了为什么要让三个安装入口共用分类目录，以及为什么 Codex 保留兼容清单。[后续子模块决策](../agents/adr/0002--upstream-submodule-references.md)修改了其中的外部引用方式，同时保留其余打包选择。这样，读者可以分清哪些理由仍有效，哪些部分已经被替代。

## 怎样提出请求

在目标项目中，可以先记录尚未实施的设计讨论。示例使用本项目的 Codex 插件。

```text
$skills:project-adr
我们正在比较上传文件的本地存储和对象存储方案。
讨论中及时保存重要约束、已评估方案、否决理由和未决问题。
复用这个议题已有的记录。目前尚未选定方案，不实施存储改动。
```

用户或获授权的 agent 已经选定方案，但实施尚未完成时，默认状态为 `accepted`。仅提出建议时仍为 `proposed`。例如，可以要求“已选定对象存储，以后再实施。记录选择、理由和剩余工作”。

已有记录或实现发生变化时，可以提出维护请求。

```text
$skills:project-adr
检查本项目关于上传文件保存位置的现有决策。
如果选择已经改变，写清新理由和真实备选方案，维护新旧记录的链接。
如果只是代码路径改变，同步原记录的事实。
先展示准备修改的文件，不归档或删除其他记录。
```

单独安装时使用 `$project-adr`。Claude Code 插件中使用 `/skills:project-adr`。普通讨论和外部访谈技能都遵守相同的项目规则，复用同一议题的记录，无需修改外部技能。

开始提出或实施相关方案前，助手先检索活跃记录，读取已有选择、否决理由和未决问题。条件变化可以成为重新评估的依据，原有理由仍需保留。`project-adr` 负责记录，`project-engineering` 负责在调查和实施时触发读取及同步。持续生效还需要完成[项目接入](../../skills/engineering/project-adr/references/PROJECT-INTEGRATION.md)，仅安装技能并不足够。

## 会生成什么文件

助手先找已有记录和项目模板。检索依据仍然有效时，后续步骤复用这份议题上下文。任务范围、约束、能力、路径、检索词、证据或相关记录发生变化，导致原检索可能不完整时，需要重新检索。候选评估、未决问题和待定方案的首次选定继续保存在原议题记录中。替换已经选定的方案时，遵循项目的替代规则。默认新建互相链接的后继记录，原方案尚未实现时也适用。

项目完全没有约定时，一个决策议题放在一个 Markdown 文件中，相关候选方案及其结论放在一起。被拒方案具有独立的长期价值时，才单独记录。默认路径如下。

```text
docs/adr/NNNN--kebab-title.md
```

例如 `docs/adr/0001--upload-storage.md` 是一个示例文件名，不会因为调用 Skill 就固定创建。归档的缺省位置是 `docs/adr/archive/`。本集合已经明确使用 `docs/agents/adr/`，因此维护本集合时沿用该目录。

下面用一个尚未选定方案的虚构存储讨论演示默认英文结构。实际理由和备选方案需要来自证据。尚未确定的候选方案无需编造否决理由。

```markdown
# Upload storage

Status: proposed

## Problem
Uploads need durable retention and a clear deletion owner.

## Decision
Local and object storage remain under evaluation. Deletion ownership is open.

## Alternatives
Local storage needs a backup assessment. Object storage needs a cost assessment.
Both candidates remain pending.

## Consequences and risks
Retention, deletion behavior, and operating costs still need verification.
```

`proposed` 表示仍在评估，`accepted` 表示已经选定但尚未完成实施，`implemented` 表示已经完成实施且有证据。`rejected` 保存仍有预防价值的被拒提案，`superseded` 表示被完全替代，`archived` 表示冻结的历史。议题中可以包含被拒候选方案，整个议题不必标为 `rejected`。接受方案本身不授予执行权限。项目已有状态体系时，继续遵守项目体系。

项目没有生命周期约定时，助手才读取[默认状态定义](../../skills/engineering/project-adr/references/LIFECYCLE.md#default-states)。归档或删除记录前，再读取单独的[内容保留和依赖检查](../../skills/engineering/project-adr/references/LIFECYCLE.md#archive-or-delete)。

## 实现变化后怎样维护

文件移动、配置键改名，但选择没变，就更新原记录中的事实。选择变了，就保留旧记录所代表的决定，并建立新旧关系。部分替代时，两份记录还可能各自负责一部分理由，不能为了整齐把旧内容全部删掉。

归档和删除需要符合任务授权。归档正文保持冻结。助手也不应为了填满模板编造备选方案；无法恢复的历史应写明缺口。

## 怎样验收

先读记录能否解释选择，再运行机械检查。检查器只验证默认结构、状态和本地链接路径，不会判断理由是否真实。

在本集合根目录，可以执行下面的命令检查本集合的记录。

```sh
python3 -B skills/engineering/project-adr/scripts/check_adr.py docs/agents/adr
```

它会读文件并报告结果，不会替你生成 ADR。默认检查器也兼容完整的中文结构，但不能用它强行改造另一个项目的有效模板。详细约定见[执行指令](../../skills/engineering/project-adr/SKILL.md)和[项目接入流程](../../skills/engineering/project-adr/references/PROJECT-INTEGRATION.md)。

交接设计讨论时，还要检查下一个 agent 能否找到议题、恢复真实否决理由、区分已选结论与建议，并在没有原聊天的情况下找到下一个未决问题。格式检查通过不能证明这些行为。
