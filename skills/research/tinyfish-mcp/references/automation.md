# TinyFish automation workflows

Read only the section matching the selected automation branch. Use the live TinyFish MCP schema for available names and arguments.

## Automation goals

Use `run_web_automation` when interaction is necessary. State the target site, required actions, constraints, and observable result in a precise natural-language goal. For structured output, specify fields, types, units, and missing-value handling.

Example goal:

```text
Extract all plans as JSON with name, price, currency, and features.
Use null for unpublished prices and retain each plan's source URL.
```

Inspect returned data and page evidence. Completion requires the requested actions and result to be verified, with failed or unreadable parts reported. Submitting a form or performing another external action still requires matching user authorization.

## Asynchronous runs

Use `run_web_automation_async` for long-running workflows when exposed by the server.

1. Keep the returned run ID.
2. Use `get_run` to retrieve that run's status and result. Continue observing a pending run instead of starting a duplicate.
3. Use `cancel_run` if the run is no longer needed and cancellation is available.
4. Inspect the final result against the goal. Report terminal failures or an unresolved pending state accurately.

## Batch jobs

Prefer exposed batch tools for multiple independent automation jobs: `batch_create`, `batch_status`, and `batch_cancel`. Keep unrelated sites or workflows as separate jobs with their own goals.

Retain the returned batch and job identifiers, check each job's result, and cancel only work no longer needed. A completed batch does not establish that every job succeeded; report the completed and failed portions separately.

## Raw browser sessions

Use `create_browser_session` only when raw browser/CDP control is required and the environment can connect to the returned session. Ordinary interaction belongs to the automation goal workflow.

Confirm connectivity before relying on the session. Inspect actual page state after actions. Release sessions you created when finished if the exposed contract supports release; otherwise report the remaining session state rather than inventing a cleanup tool.
