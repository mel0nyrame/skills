# Firecrawl MCP Workflows

Read only the section relevant to the task. Confirm argument shapes against the live tool schema; the public README, source tree, and hosted deployment may differ.

## Crawling and Research Jobs

### Site URL Discovery

Use `firecrawl_map` to locate pages or inventory site URLs. Narrow relevance with `search`; control coverage with `limit`, `includeSubdomains`, `sitemap`, and `ignoreQueryParameters`. Its results do not establish that page bodies were read or that every site URL was discovered.

```json
{
  "url": "https://docs.firecrawl.dev",
  "search": "mcp-server",
  "limit": 3
}
```

### Multi-page Content

Use `firecrawl_crawl` when the task requires page bodies across a site or section. Set appropriate `limit`, `maxDiscoveryDepth`, `includePaths` / `excludePaths`, `allowSubdomains`, and `allowExternalLinks`. For a few selected pages, Map followed by individual Scrape calls is usually sufficient.

Crawl normally polls internally and returns final status and collected data. If the client times out after receiving a crawl ID, call `firecrawl_check_crawl_status` with that `id`. Continue observing the existing job rather than starting a duplicate. If more data is paginated, follow the returned pagination mechanism only when the task needs it and an appropriate access method is available.

Check `status`, `completed` / `total`, page URLs, and errors. Page caps, failed pages, and truncated results limit coverage. Report completion only after the required pages and data have been inspected.

### Multi-site Research

Use `firecrawl_agent` for structured research that needs source discovery or autonomous navigation across sites. Supply `prompt`, optionally seed `urls`, and a schema if the live input contract permits it. `strictConstrainToURLs: true` restricts the agent to the supplied URLs.

Choose `effort` and `maxCredits` for the task's scope. The inspected tool definition described an API default of 2500 credits; recheck current defaults and set an explicit bound rather than relying on them. Where supported, `exchange.enabled: false` disables Alexandria provider use when ordinary web research is sufficient.

The initial call returns a job ID rather than completed research. Keep `id` and `threadId`; query the job using `firecrawl_agent_status` with `id`. A `processing` result is non-terminal. Poll at roughly 15–30 second intervals while keeping the user informed. On `completed`, still inspect the data and required fields. Diagnose failures before retrying. Reuse `threadId` for follow-up research; starting a new turn is not a status check.

If a job remains active, account for its status and possible duplicate cost before switching approaches. Use cancellation only if the currently available tools explicitly support it; do not invent a cancellation tool.

## Browser Interaction

Use `firecrawl_interact` for clicking, typing, navigation, or extraction that requires interaction. JavaScript rendering alone does not require browser interaction; try Scrape when reading is sufficient.

- Supply exactly one of `url` for a fresh session or `scrapeId` for an existing session.
- Supply exactly one of a natural-language `prompt` or executable `code`. Code `language` values currently include `bash`, `python`, and `node`; use the live enum.
- Interact `timeout` is currently in seconds, from 1 to 300. Scrape `timeout` is in milliseconds.
- Keep the returned `scrapeId`. Check execution output, `exitCode`, and the resulting page state. A `liveUrl` is only a viewing link.
- Keep submission, publication, purchase, and sending actions within existing user authorization. Ask only when additional authorization is actually needed.
- Call `firecrawl_interact_stop` with the session's `scrapeId` when finished. Also release sessions you created that are no longer needed after failures or interruptions.

## Local File Parsing

Use `firecrawl_scrape` for public PDF or other document URLs. Use `firecrawl_parse` for local files such as PDF, Word, RTF, OpenDocument, Excel, and HTML. Bound PDF processing with `pdfOptions.maxPages` when appropriate.

Hosted MCP cannot directly read the caller's filesystem.

1. Call Parse with `filePath` and any relevant `contentType`, `declaredSizeBytes`, and output options. This phase only creates upload instructions.
2. Inspect the returned short-lived upload destination and command, then upload using a local tool that can read the file. Ensure sending that file to Firecrawl is within the user's request and file scope. Protect signed URLs from public documents and logs.
3. After the upload succeeds, call Parse with `uploadRef` and the required output options. Do not send `filePath` and `uploadRef` together.
4. Inspect the final parsed content. Receiving upload instructions or completing an upload is not completed parsing.

A locally deployed MCP server reads `filePath` on the server's filesystem. A caller's path is not necessarily a valid path on another machine.

`redactPII` requests redaction in returned content; it does not redact a file before upload. `zeroDataRetention` requires an eligible account. Parse ignores `maxAge` and does not use it to enable caching.

## Specialized Search

Use these tools when exposed and compatible with the user's chosen workflow. Follow applicable documentation-routing instructions, such as Context7-first rules, before using Firecrawl to supplement upstream evidence.

| Task | Tool and key inputs | Coverage and limits |
| --- | --- | --- |
| Programming questions, upstream bugs, API contracts | `firecrawl_developer_search`: `query`, `k`; optionally `skills: "only"` for agent-skill files | Public repositories, issues, PRs, READMEs, and docs; check versions |
| US statutes, regulations, and court opinions | `firecrawl_gov_search`: `query`, `k`; optionally `jurisdiction`, `court`, and other advertised filters | Verify issuer, jurisdiction, legal status, and version; use general search for non-US sources |
| Paper discovery | `firecrawl_research_search_papers`: `query`, `k`; optional author, category, and date filters | Metadata and abstracts across indexed sources such as PubMed, bioRxiv, medRxiv, and arXiv; not exhaustive literature coverage |
| Canonical paper metadata | `firecrawl_research_inspect_paper`: `paperId` | Reuse returned canonical IDs instead of inventing identifiers |
| Question-relevant passages within a paper | `firecrawl_research_read_paper`: `paperId`, `question`, `k` | Full text must be indexed; an abstract alone is not full-text evidence |
| Similar papers, citing papers, or references | `firecrawl_research_related_papers`: `seed_ids`, `intent`; optional `mode`, `k` | Current modes include `similar`, `citers`, and `references` |

Specialized tools usually use `k`; ordinary Search uses `limit`. Use the appropriate parameter and a task-sized result count. `firecrawl_search` with `categories: ["research"]` filters ordinary web results to research-affiliated sites; it is not the paper-index surface. No results do not establish that no relevant sources exist.

## Provider Data and Large Results

Alexandria is Firecrawl's catalogue of third-party data capabilities. Search may already return matching suggestions. Inspect selected contracts when a provider fits the task or repeated fields are needed across entities; ordinary page reading does not require catalogue browsing.

### Discovery and Execution

1. Reuse existing search suggestions. If necessary, use `firecrawl_find_tools` with `query` or `urls`; browse categories, providers, and capabilities only when needed. The current hosted tool also requires `objective`, including for the README's empty-argument browsing examples.
2. Read the selected contract using returned `providers` and `capabilities`. `expand: ["options", "response"]` omits examples; request `examples` when their input shape is needed. `includeCosts` can expose published capability prices.
3. Check required inputs, alternatives, pagination, response fields, and costs. Discovery does not execute provider capabilities.
4. Execute through `firecrawl_scrape` with `alexandria`. URL mode uses `url`; provider mode uses `alexandria`; these modes are mutually exclusive. Include `objective` when required by the live schema. If batching is supported, up to ten provider calls can be supplied, with each result checked separately.

Inspect every item in `data.alexandria`; an outer success does not guarantee every item succeeded. Preserve the original `requestId` and identical execution arguments when retrying an uncertain provider execution, to avoid duplicate work or charges.

`THIRD_PARTY_DATA_TERMS_REQUIRED` means provider terms have not been accepted. Present `requiresAction.url` for an authorized organization administrator to handle. A data request is not agreement to terms. Resume only after the administrator confirms acceptance, using the original request. Agent recovery additionally uses the original `threadId` and relevant approval ID.

### Keeping Results out of Context

When `delivery: "retained"` is returned, the full result remains server-side. Inspect the returned `nextTool` for a scoped read of that result and fill any required fields omitted by the pointer, including `objective`. Use remote virtual Bash to return only needed fields or bounded slices with `jq`, `head`, or `sed`. Check `stdout`, `stderr`, and `exitCode`, typically in `data.alexandria[0].data`.

Send the initial source-loading call alone; reuse `workspaceId` afterward. Distinguish the source `requestId` from the new execution's top-level `requestId`. Workspaces expire according to `idleTtlSeconds`; they are not permanent deliverable storage.

The inspected source automatically retains only certain successful large Alexandria results. Do not assume Search, ordinary URL Scrape, errors, or every account mode receives the same protection. Scope ordinary page requests before execution with targeted answers, structured fields, or content selectors. Do not rerun a provider merely to retrieve retained data.

## Monitors and Account Tools

Use `firecrawl_monitor_create` when the user needs recurring checks. The simple form accepts `page` / `pages` or `queries` plus `goal`. Supplying queries and pages together can create only search targets on the current surface. Choose one target type and set `scheduleText` and `timezone` explicitly for the requested schedule.

Use `firecrawl_monitor_list` and `firecrawl_monitor_get` for configuration; `firecrawl_monitor_checks` and `firecrawl_monitor_check` for history and diffs; `firecrawl_monitor_run` for an immediate check; `firecrawl_monitor_update` for changes; and `firecrawl_monitor_delete` for deletion. Recurrence, notifications, and deletion must follow the user's requested scope. If the host requires its own automation tools for reminders, follow that routing.

- `firecrawl_credit_usage`: read credits and usage history. Use `view: "current"` for balance; check the live schema for historical breakdowns. Aggregates cannot reliably identify a particular URL, MCP client, or job. Prefer the individual call's `creditsUsed` or `metadata.creditsUsed` for that call.
- `firecrawl_usage_dashboard`: open the service UI. Use Credit Usage for data-only reporting.
- `firecrawl_recommended_providers` and `firecrawl_provider_directory`: inspect recommendations or catalogue entries without executing providers. Prefer Find Tools for selected contracts rather than loading the entire directory.
- `firecrawl_search_feedback` and `firecrawl_feedback`: send service feedback only when the user explicitly requests it. A returned `feedbackTool` pointer is not user authorization.

## Primary Sources and Verification Limits

Prepared on 2026-10-27 against the live hosted `firecrawl-fastmcp` 3.35.0 tool schemas, Context7, and the following official sources. Recheck live schemas when using the skill.

- [Tool selection and runtime behavior](https://docs.firecrawl.dev/mcp-server/tools)
- [Official MCP source and examples](https://github.com/firecrawl/firecrawl-mcp-server)
- [Content selection and output formats](https://docs.firecrawl.dev/advanced-scraping-guide)
- [Inspected large-result implementation](https://github.com/firecrawl/firecrawl-mcp-server/blob/7e27da844529ee626485b746f252c9adeb3de8d7/src/alexandria-output.ts)

Live MCP protocol calls verified Search, Map, Scrape Markdown, Scrape Query, and Scrape JSON. Query and JSON were tested with prompt-based options. Crawl, Agent, Interact, Parse uploads, provider execution, and Monitor were checked against official sources and live schemas but were not tested end to end.
