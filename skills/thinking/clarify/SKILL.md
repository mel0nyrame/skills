---
name: clarify
description: Use when the user asks to clarify intent or stress-test an open-ended question before receiving an answer. Ask one decisive question when a decision-changing gap remains; otherwise answer directly.
---

# Clarify

Check whether the supplied context leaves a decision-changing gap before answering. Use a two-stage conversation when clarification is needed. Present concise, verifiable conclusions without revealing private chain-of-thought.

## Stage 1: Analyze and pause

Assess the supplied context without tools or file changes. A gap matters only when plausible answers would change the recommendation, conclusion, scope, or priority.

If no such gap remains, briefly state that the supplied context is sufficient and proceed to Stage 2 in the same reply. Ask no question solely to fill the format.

If a gap remains, produce these sections in order. Omit the mistake section when no relevant mistake or risk is supported:

1. **Hidden assumptions**: Identify the main unstated conditions on which the question depends. Distinguish reasonable inferences from assumptions that still need validation. Never present guesses as facts.
2. **Critical information gaps**: List only missing information that could materially change the recommendation, conclusion, scope, or priority. Briefly explain how plausible answers would change the final response.
3. **Relevant mistake or risk**: Identify one mistake supported by the context, or label a plausible concern as a risk. Tie it to the user's situation without inventing its prevalence or the user's behavior.
4. **One decisive question**: Select the single highest-information-gain question from the gaps above and ask only that question.

Stop immediately after the question and wait for the user's reply. Do not provide a final answer, plan, or substantive recommendation during this stage. Do not execute tools or modify anything during this stage.

Use this compact format:

```markdown
Hidden assumptions

- ...

Critical information gaps

- ...; if A, the answer would ...; if B, it would ...

Relevant mistake or risk (when supported)

- ...

One decisive question

...
```

## Question constraints

- Prioritize the user's real objective, success criterion, concrete context, or strongest constraint.
- Ask a question whose answer will materially narrow or change the final response.
- Ask about one decision dimension and use only one question mark.
- Never bundle subquestions with words such as “and,” “also,” or “respectively.”
- Do not repeat information the user already supplied.
- Offer a few mutually exclusive choices when that makes the question easier to answer, but still request only one choice.

## Stage 2: Deliver the final answer

After the user answers the decisive question, or the initial assessment finds no decision-changing gap:

1. Use the original request and any clarification received.
2. State only the remaining assumptions that materially affect the result.
3. Answer the user's actual goal directly.
4. Prefer specific, actionable guidance with explicit tradeoffs over generic advice.
5. Do not start another clarification round unless the reply reveals an ambiguity that makes a safe or correct answer impossible.

If another clarification is strictly necessary, ask exactly one decisive question and pause again.
