---
name: clarify
description: Use when the user asks to clarify intent or stress-test an open-ended question before receiving an answer. Ask one decisive question when a decision-changing gap remains; otherwise answer directly.
---

# Clarify

Check the supplied context for a decision-changing gap before answering. Use only that context during the initial intent check, without tools or file changes. A gap matters when plausible answers would change the recommendation, conclusion, scope, priority, or authorization.

## Context is sufficient

Answer directly in the same reply. State only assumptions that materially affect the result; omit a sufficiency announcement and clarification headings.

## A decision-changing gap remains

1. Briefly explain the missing condition and why its answer changes the result. Mention a hidden assumption or relevant risk only when it helps the user answer; distinguish supported facts from possible risks.
2. Ask one decisive question once, about the highest-value missing decision dimension. When useful, follow it with mutually exclusive choices stated as options rather than another question.
3. Stop and wait for the reply. Keep substantive recommendations, plans, tool use, and file changes for after this question is resolved.

Complete this stage when one question identifies the decision the user needs to make, without bundling unrelated questions or repeating supplied information. Use headings only when they improve readability; no fixed report template is required.

## After the user's reply

Use the answer with the original request to give a specific, actionable response. Preserve material tradeoffs and uncertainty without exposing private chain-of-thought. Later actions follow the task's authorization; clarification alone authorizes no file changes.

Ask again only if the reply leaves an ambiguity that prevents a correct or safe response. In that case, ask exactly one decisive question and pause.
