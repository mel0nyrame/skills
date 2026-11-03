---
name: clarify
description: Use when the user asks to clarify intent or stress-test an open-ended question before receiving an answer. Identify decision-changing gaps, ask one decisive question, and wait for the reply.
---

# Clarify

Use a strict two-stage conversation: calibrate the question first, then answer it. Present concise, verifiable conclusions without revealing private chain-of-thought.

## Stage 1: Analyze and pause

Before answering the user's underlying question, produce these four sections in order:

1. **Hidden assumptions**: Identify the main unstated conditions on which the question depends. Distinguish reasonable inferences from assumptions that still need validation. Never present guesses as facts.
2. **Critical information gaps**: List only missing information that could materially change the recommendation, conclusion, scope, or priority. Briefly explain how plausible answers would change the final response.
3. **Most common mistake**: Identify exactly one mistake that commonly sends this type of problem in the wrong direction. Tie it to the user's situation.
4. **One decisive question**: Select the single highest-information-gain question from the gaps above and ask only that question.

Stop immediately after the question and wait for the user's reply. Do not provide a final answer, plan, or substantive recommendation during this stage. Do not execute tools or modify anything during this stage.

Use this compact format:

```markdown
Hidden assumptions

- ...

Critical information gaps

- ...; if A, the answer would ...; if B, it would ...

Most common mistake

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

After the user answers the decisive question:

1. Combine the new information with the original request.
2. State only the remaining assumptions that materially affect the result.
3. Answer the user's actual goal directly.
4. Prefer specific, actionable guidance with explicit tradeoffs over generic advice.
5. Do not start another clarification round unless the reply reveals an ambiguity that makes a safe or correct answer impossible.

If another clarification is strictly necessary, ask exactly one decisive question and pause again.
