# Manual scenarios for recap terminology and knowledge profiles

These scenarios evaluate the [recap entry point](../../skills/knowledge/recap/SKILL.md), [glossary rules](../../skills/knowledge/recap/references/glossary.md), and [profile rules](../../skills/knowledge/recap/references/profile.md). They are expected behaviors, not recorded model-test results. Structural checks and a helper publication smoke test do not establish inference accuracy.

Use a disposable knowledge library and an explicitly selected synthetic conversation. Supply each message's speaker, position, and date, with the complete selected range. Keep synthetic content clearly labeled. Provide an inspected harness fixture whose tool catalogue contains `read_file`, `search`, and `exec`; its search returns paths without executing commands. This fixture defines only that harness. Give the agent the current recap skill and resources. Authorize capture into the temporary library; query scenarios authorize no formal updates.

## Recognize components with limited evidence

User message:

```text
This harness contains read_file, search, and exec.
```

Request a capture. Check that the knowledge profile records recognition of those components, links the exact user message, and leaves scheduling/recovery understanding unknown. The profile uses `type: research` and alias `knowledge profile`. The source and profile publish through the normal candidate flow. No unrelated personality claims or competence score should appear.

Check the artifact report against disk: the chosen profile path under `topics/`, its source record under `sources/`, catalog and changelog updates, and the operation's publication record. The report distinguishes additions and updates. With a second supported capture, the same profile path gains an entry instead of creating a conversation-named profile. Initializing the empty fixture alone must not create profile or glossary topics.

## Explain a mechanism and apply it

User messages:

```text
Search returns paths; exec runs commands. A search hit does not execute the file.
To inspect a matching function without running the program, I would first search
for its name, then read the matching file.
```

Request a capture. Check that recognition, understanding of this separation, and application to this inspection task are distinguished. Later reuse may use familiar tool names directly. It still explains new scheduling or recovery mechanisms when they matter.

## Attribute repeated or incorrect statements

The assistant lists the three tools. The user quotes that list and says “yes.” A later user message says “search executes each file it finds,” contrary to the supplied catalogue.

Request a capture. Check that quotation/agreement does not become evidence of independent explanation. Preserve the incorrect mechanism claim and its correction without promoting it to mechanism understanding. Attribute each statement to its speaker and retain uncertainty about broader competence. The existence of assistant-written tool documentation cannot fill that gap.

## Scope glossary definitions and preserve readable topics

The user explicitly defines `agent = harness + AI` as shorthand for this set of notes. Another source uses “agent” for a different scoped concept.

Request capture of those resolved definitions and a topic using the first definition. Check that the glossary is a `concept` topic with alias `glossary`, preserves context differences, and defines or links `harness` and `AI`. The topic introduces the necessary local meaning with a direct entry link and retains essential reasoning and conditions. Read its prerequisite links without the conversation; missing or circular definitions need repair before publication.

## Correct evidence and consume the result in a query

Start with published fixture glossary/profile topics. Correct an attributed source statement or narrow its applicability. Request maintenance, then query the topic with an explanation adapted to the profile using only the library's current content.

Check that maintenance reconciles dependent profile interpretations while retaining unrelated supported entries and sources. The query discovers the resources through their aliases, reads the relevant current topics at a consistent revision, and selects explanation depth within the supported scope. New user statements during this query do not update formal profile claims. Compare the formal Git revision and tracked bytes before and after; search cache/lock writes are allowed.

## Query without personalization resources

Use a library with an ordinary sourced topic and no glossary or profile. Request a personalized explanation without formal updates.

Check that the agent tries relevant titles/aliases, then uses the topic's own definitions and explains prerequisites normally. It should neither invent a profile nor initialize new resources. Ordinary conversation outside an explicit recap invocation should not trigger capture.

## Load only the selected branch

Record which instruction files the agent reads for each request in a fresh context:

| Request | Expected reading route |
| --- | --- |
| Find a topic's recorded version; no personalization | Entry point → query → search; capture/profile instructions are not required |
| Capture a resolved term with no understanding evidence | Entry point → capture; glossary → shared storage; profile instructions are not required |
| Capture useful user-understanding evidence without new terminology | Entry point → capture; profile → shared storage; glossary instructions are not required |
| Explain a topic according to the user's profile | Entry point → query; profile use → shared discovery; source-extraction and publication instructions are not required |

Capture also follows its source, writing and publication pointers. A concrete error or linked prerequisite can justify more reading; record the reason rather than treating every linked file as required. Compare the first request's formal revision and tracked bytes before/after to confirm it remains query-only. File routing checks alone do not establish that a model follows these paths.
