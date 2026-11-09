# Retro 怎样复盘一次编码会话

[English](retro.md) | 简体中文 · [全部指南](../README.zh.md)

这是 [Matt Pocock 上游 retro Skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/retro) 的使用说明。它复盘一次编码会话中的 Agent 环境。它按严重程度给出改进建议，不修改被检查的代码。

这个 Skill 只在你显式调用时运行。它检查导航、自动检查、编码规范、全局 `AGENTS.md`、工具使用、空操作和信息获取。然后按严重程度列出候选建议，由你选择。

## 先安装它和配套写作参考

它属于外部 Skill，不包含在本集合安装的 9 个 Skill 中。可以单独安装。

```sh
npx skills@latest add mattpocock/skills --skill retro
```

它的第一步会调用上游 `writing-for-agents` Skill，取得写作风格指南。两个 Skill 都要安装。

```sh
npx skills@latest add mattpocock/skills --skill writing-for-agents
```

选择 Codex 作为安装目标后，可以使用 `$retro`。本集合的[子模块](../../skills/engineering/retro)记录的是上游仓库引用，不等于已安装这个 Skill。

## 怎样得到一份可检查的复盘

```text
$retro
复盘这次会话里的 Agent 环境。按你检查过的类别组织发现，
按严重程度排序候选建议，并说明每项为什么值得改。
只提出建议，不修改文件，不 commit 或 push。
```

这是教学示例。实际使用时把范围换成你要复盘的会话。

## 产物与验收

| 你的请求 | 应有产物 |
| --- | --- |
| 显式调用 `$retro` | 对话里按严重程度排序的建议 |
| 明确保存笔记 | 对应本地文件，完成后应重新打开核对 |
| 采纳某项建议 | 另一次明确授权的实现请求 |

检查建议能否让没参加会话的人看懂问题类别、观察到的现象和建议的改法。没有单独授权时，不应有任何文件变动。

配套 Skill 见 [writing-for-agents 使用指南](writing-for-agents.zh.md)。上游完整指令和署名见[原文](https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md)及[第三方通知](../../THIRD_PARTY_NOTICES.md)，本页不保存其指令副本。
