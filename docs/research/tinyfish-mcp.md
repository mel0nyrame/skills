# TinyFish MCP for pages that need reading or interaction

English | [简体中文](tinyfish-mcp.zh.md) · [All guides](../README.md)

`tinyfish-mcp` guides web discovery, content reading, and browser tasks assigned to the configured TinyFish MCP server. Select it when you want TinyFish; an explicit request for another service keeps that choice. Prefer lightweight reading when the page already exposes the content. Browser automation becomes useful when filters, clicks, or dynamic loading are necessary.

A concrete task might filter a supplied course catalog to online courses and collect names, fees, and sources. The actions remain bounded by your request.

## Prepare the connection

Configure a TinyFish MCP server and confirm its tools appear in the current session. This skill does not create accounts, connect the service, or supply credentials. Available names and arguments depend on the live connection.

If the agent supports HTTP MCP, configure it through the agent's MCP server settings. The skill's [connection metadata](../../skills/research/tinyfish-mcp/agents/openai.yaml) declares this endpoint. It is the tool connection address, distinct from the course-page URL you will supply. Complete authentication, then confirm tools can be called in the session.

```text
https://agent.tinyfish.ai/mcp
```

A login-protected page also needs appropriate access in the browser task. The ability to click a button does not authorize registration, purchases, or sending information.

## Specify browser actions and saving together

This is a teaching example. Supply a real course-catalog URL.

```text
$skills:tinyfish-mcp
Open the course catalog I provide and filter for online courses. Extract course
name, fee, currency, and course URL into data/online-courses.json. Use null for
unavailable fees and report unreadable pages. Do not register, buy, or submit forms.
```

This uses the collection's Codex plugin. Use `$tinyfish-mcp` standalone or `/skills:tinyfish-mcp` in Claude Code. Replace the saving instruction with a chat-only result if no file is needed.

## Follow the task through

The assistant checks whether the URL can be read directly. Sufficient content needs no separate browser session. When interaction is necessary, the automation goal should specify it precisely.

A long job may initially return a run ID, the service's identifier for that execution. Check the same run rather than starting another because it remains active. Use an available cancellation operation when cancellation is needed.

The assistant reads the relevant [automation workflow](../../skills/research/tinyfish-mcp/references/automation.md) before starting interaction, an asynchronous run, batch jobs, or a raw browser session. Ordinary page reading uses the main tool-selection rules without loading every automation branch.

Returned data still needs checking. Confirm that filters actually took effect, links match the courses, and fees came from pages. A successful click alone cannot prove the requested filter worked.

## Outputs and their locations

| Location | Contents |
| --- | --- |
| Conversation | Completed actions, extracted results, sources, and failure scope |
| TinyFish service | Run identifier and status when the selected tool provides them |
| `data/online-courses.json` | Created only when the saving instruction is executed with local writing capability |

This illustrates the file structure, not actual course data.

```json
[
  {
    "name": "<page title>",
    "fee": null,
    "currency": null,
    "url": "<course URL>"
  }
]
```

The skill has no fixed output directory and does not automatically create browser recordings, screenshot collections, or a scraping database. Service-hosted file URLs and actual local save paths need separate identification.

## Check whether the result is usable

Sample course pages to verify the online-course condition and missing-value report. Inaccessible pages remain gaps. Login screens, empty pages, and error responses are not course content.

Missing tools should be reported. If another service is used, identify the actual provider. Consult the [execution instructions](../../skills/research/tinyfish-mcp/SKILL.md) for selection and run tracking, or the [Firecrawl guide](firecrawl-mcp.md) for that alternative connection.
