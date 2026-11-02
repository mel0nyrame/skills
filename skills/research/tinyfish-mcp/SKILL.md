---
name: tinyfish-mcp
description: Use the TinyFish MCP server for live web search, fetching URLs, current information, source-backed research, page extraction, scraping, and browser automation. Activate when the user asks to search, find, look up, research, compare, verify current information, read or summarize a URL, extract web content, or interact with a website.
---

# TinyFish MCP

Use the tools exposed by the configured TinyFish MCP server instead of the TinyFish CLI.

Do not run `tinyfish` shell commands when the TinyFish MCP tools are available.

## When to Use This Skill

Activate this skill when the user:

- Asks to search, find, look up, research, or compare information on the web.
- Needs current or recently changed information.
- Wants information verified against live web sources.
- Provides a URL and asks to read, summarize, inspect, or extract information from it.
- Needs structured data extracted from a website.
- Needs interaction with a website such as navigating, clicking, filling forms, or working with dynamic pages.

## Tool Selection

Use the lightest TinyFish MCP tool that can complete the task.

```text
search
  ↓
fetch_content
  ↓
run_web_automation
  ↓
create_browser_session
```

### `search`

Use for discovery and live web search.

Typical uses:

- Find relevant URLs.
- Find current documentation.
- Check current pricing or product information.
- Find recent news or changing information.
- Gather sources before deeper research.

When the search result itself contains enough information to answer the request, do not fetch pages unnecessarily.

For research tasks, normally search first and then fetch the most relevant primary or authoritative sources.

### `fetch_content`

Use when one or more URLs are already known and their page content is needed.

Typical uses:

- Read an article or documentation page.
- Summarize a URL supplied by the user.
- Extract clean page text.
- Inspect product or pricing pages.
- Retrieve content from multiple independent URLs.

Prefer `fetch_content` over browser automation when merely reading the page is sufficient.

When several independent URLs need to be read, fetch them together when the tool supports it rather than making unnecessary sequential calls.

### `run_web_automation`

Use when the task requires actual interaction with a website.

Typical uses:

- Navigate through multiple pages.
- Click controls.
- Fill or submit forms.
- Apply filters.
- Work with dynamic web applications.
- Extract data that cannot be obtained reliably through `fetch_content`.

Provide a precise natural-language goal.

When structured output is required, explicitly describe the desired output schema in the goal.

Example goal:

```text
Extract all plans as JSON:
[
  {
    "name": "string",
    "price": "string",
    "features": ["string"]
  }
]
```

Do not use web automation for a task that `search` or `fetch_content` can solve.

### `run_web_automation_async`

Use the asynchronous automation tool for long-running web workflows when it is available.

After starting the run:

1. Keep the returned run ID.
2. Use `get_run` to retrieve its status and result.
3. Use `cancel_run` if the run is no longer needed.

Do not start duplicate runs simply because a run is still in progress.

### Batch Automation

For multiple independent automation jobs, prefer TinyFish batch tools when available:

- `batch_create`
- `batch_status`
- `batch_cancel`

Keep independent sites or workflows as independent jobs rather than combining unrelated tasks into one large automation goal.

### `create_browser_session`

Use only when raw browser/CDP control is actually required and the environment can connect to the returned browser session.

Prefer `run_web_automation` for normal website interaction.

Do not create a raw browser session merely to read a page or perform a straightforward extraction.

## Research Workflow

For ordinary web research:

```text
search
  ↓
select relevant sources
  ↓
fetch_content
  ↓
synthesize the answer
```

Prefer:

1. Primary sources.
2. Official documentation.
3. Original announcements or publications.
4. High-quality secondary sources when primary sources are unavailable.

For claims that may have changed recently, verify them against live sources rather than relying on model knowledge.

## Escalation Rules

Escalate only when the lighter tool is insufficient.

```text
Need URLs or current facts
→ search

Have URL and need page content
→ fetch_content

Need interaction or dynamic extraction
→ run_web_automation

Need low-level browser control
→ create_browser_session
```

If `fetch_content` returns incomplete content because a site requires interaction, escalate to `run_web_automation`.

Do not escalate merely because a heavier tool is available.

## MCP Tool Names

Use the tools belonging to the configured TinyFish MCP server.

Depending on the MCP client, tools may appear with a server-specific prefix. Match the TinyFish tool by its exposed tool name rather than assuming an exact generated prefix.

Common TinyFish MCP tools include:

```text
search
fetch_content

run_web_automation
run_web_automation_async
get_run
list_runs
cancel_run

batch_create
batch_status
batch_cancel

create_browser_session
list_browser_sessions
```

Additional TinyFish tools may be exposed by the server. Use them when their advertised schema clearly matches the task.

Do not invent MCP tool names or arguments. Use the schema exposed by the MCP server.

## General Rules

- Use TinyFish MCP rather than the TinyFish CLI when the MCP server is available.
- Match the user's language in the final response.
- Prefer the lightest sufficient tool.
- Search before fetching when the correct URL is unknown.
- Fetch directly when the user already supplied the URL.
- Prefer authoritative sources for factual claims.
- Preserve source URLs needed to support the final answer.
- Do not claim that a search, fetch, or automation succeeded unless the MCP tool actually returned a successful result.
