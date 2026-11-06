# Firecrawl MCP for web results you can check

English | [简体中文](firecrawl-mcp.zh.md) · [All guides](../README.md)

`firecrawl-mcp` guides use of connected Firecrawl tools for finding pages, reading known URLs, extracting fields, and, when necessary, interacting with dynamic pages or collecting a bounded section of a site.

Use it when you select Firecrawl or the assistant chooses Firecrawl MCP tools for the task. An explicit request for another service keeps that choice. Before Map, Crawl, or Agent operations, the assistant reads the corresponding URL-discovery, multi-page, or research subsection.

It helps turn material from several pages into a consistent result while retaining sources and checking content. Installing the skill adds instructions; the Firecrawl MCP service needs its own connection.

## Establish a working service connection

MCP is a connection through which an assistant accesses external tools. The current session must actually expose the relevant Firecrawl tools. Missing tools require a connection or session-loading explanation, not a claim that another provider's results came from Firecrawl.

This collection supplies no credentials. Authentication, credits, and tool availability depend on your connection. Begin with one or two known pages rather than an unbounded site crawl.

If your agent supports HTTP MCP connections, open its MCP server settings. This skill's [connection metadata](../../skills/research/firecrawl-mcp/agents/openai.yaml) declares the following endpoint. It is the tool-service address; supply the webpage URLs separately. Complete required service authentication, then check tool visibility in the session.

```text
https://mcp.firecrawl.dev/v2/mcp
```

## Request a concrete deliverable

This pricing-page extraction is a teaching example. It supplies no actual prices or service-cost guarantee.

```text
$skills:firecrawl-mcp
Read the two official pricing-page URLs I provide. Extract plan name, price,
currency, billing period, and source URL. Save data/pricing.csv and explain
missing fields and failed pages in chat. Do not guess unpublished prices,
submit forms, or create recurring monitors.
```

This uses the collection's Codex plugin. Use `$firecrawl-mcp` standalone or `/skills:firecrawl-mcp` in Claude Code. Supply real URLs with the request. To receive only a table in chat, replace the file-saving instruction accordingly.

## Follow the extraction

Known URLs should normally be read directly. Search is useful when sources must first be found. Inspect original pages when required fields are absent, and escalate to interaction only when clicks or dynamic loading require it.

Site collection also needs paths, page limits, and depth. A long-running task can initially return a job identifier. The assistant should retain it and check status; an identifier alone is not a completed collection.

Before Search, the assistant reads [Search requests](../../skills/research/firecrawl-mcp/references/workflows.md#search-requests). Page-specific answers and named-field extraction use [Targeted extraction](../../skills/research/firecrawl-mcp/references/workflows.md#targeted-extraction). An ordinary Markdown page read uses the main instructions without loading those examples.

Before browser interaction, local-file upload, provider execution, or another conditional operation, the assistant follows the [operation-specific reading routes](../../skills/research/firecrawl-mcp/SKILL.md#read-before-conditional-operations). Each route loads only the matching workflow.

Numbers need association with their actual plan, currency, and billing period. Generated summaries or answers require source checking before being presented as exact quotations.

## Understand where files come from

`data/pricing.csv` exists only because the example explicitly requests saving it. After receiving content, the assistant needs local file-writing capability to create it. Service success does not guarantee that a CSV appeared in your project.

The chosen fields can use this header. Actual rows must come from retrieved evidence.

```csv
plan,price,currency,billing_period,source_url
```

| Request | Main deliverable |
| --- | --- |
| Read or compare pages | An answer, table, and source links in chat; no fixed local file |
| Explicitly save CSV, JSON, or Markdown | The requested file and verified save result |
| Start asynchronous collection | A service-side job identifier, followed by status and eventual content or failure |

Screenshots, downloads, and service-side file URLs are distinct from local file paths. A saved deliverable should have an actual reported location.

## Check completion and failure boundaries

Open the CSV, follow source links, check billing periods, and confirm missing prices were not invented. Sample important values against the page. Cached content can differ from a live page; state freshness requirements in the request.

Authentication, balance, and service failures should remain explicit gaps. Incomplete reads do not justify a complete-looking comparison. Form submission, paid provider execution, and recurring monitors require matching authorization.

See the [execution instructions](../../skills/research/firecrawl-mcp/SKILL.md) for tool choice and checks, and [conditional workflows](../../skills/research/firecrawl-mcp/references/workflows.md) for jobs and files. The [TinyFish guide](tinyfish-mcp.md) describes another option when that connection is available.
