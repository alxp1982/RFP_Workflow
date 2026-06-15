---
name: spec-notion-input
description: Fetch meeting notes from Notion via MCP using one or more page URLs or a workspace search string. Writes `outputs/notion-input.md` for downstream skills. Use before `spec-normalize-input` on initial runs or as the information source for `spec-update`.
---

# Notion input — fetch meeting notes via MCP

## Purpose

Pull **meeting notes** (or other Notion pages) into the spec pipeline using the
**Notion MCP** server. Produces a single local artifact the rest of the workflow
can treat like pasted requirements text.

## Prerequisites

1. **Notion MCP** installed and OAuth completed in your AI tool (see
   **README.md** § Notion MCP and `docs/integration/notion.md`).
2. The connected Notion account must have **read access** to the target pages.
3. If Notion MCP is unavailable or auth fails, **stop** and tell the user to
   complete setup — do not invent page content.

## Inputs

Provide **at least one** of:

| Input | Example |
|-------|---------|
| **Page URL(s)** | `https://www.notion.so/myworkspace/Sprint-Planning-abc123def456…` (one or more) |
| **Search string** | `Q2 roadmap meeting notes`, `Acme discovery call` |
| **Both** | URLs to always include **plus** search to find additional pages |

Optional:

- **`mode`:** `initial` (default) — greenfield run; `update` — new info for **`spec-update`**
- **`max_pages`:** cap pages fetched (default **5** for search; no cap for explicit URLs unless user sets one)

## Instructions

You are a business analyst preparing source material for the spec workflow.

### Step 1 — Resolve which Notion pages to fetch

**If page URL(s) were given:**

1. Parse each URL and extract the Notion page id (32-char hex, with or without
   dashes). Common URL shapes:
   - `https://www.notion.so/<workspace>/<Title>-<pageId>`
   - `https://www.notion.so/<pageId>`
   - `https://<name>.notion.site/<Title>-<pageId>`
2. Record canonical URL and title when the MCP returns them.

**If a search string was given:**

1. Call the Notion MCP **search** tool (name may vary by client, e.g. workspace
   search / query) with the user's string.
2. Prefer pages that look like meeting notes (title contains "meeting", "notes",
   "workshop", "sync", "retro", "discovery", dates, etc.) but **do not** exclude
   other hits without showing them.
3. Apply **`max_pages`** after user selection (see disambiguation below).

**If both URLs and search:**

- Fetch listed URLs first, then run search and **merge** unique pages (dedupe by page id).

### Step 2 — Search disambiguation (required when search returns 2+ pages)

Before fetching body content, show a selection table:

| # | Title | URL or page id | Last edited (if available) | Include? |
|---|-------|----------------|----------------------------|----------|

Ask:
"Which pages should I pull into the spec run? Reply with numbers (e.g. `1,3`) or **all**."

**Wait for the user's reply** unless they already specified exact URLs only (no search).

If search returns **0** pages, report that and ask for a different search string or direct URLs.

If search returns **1** page, proceed without pausing unless the title clearly mismatches the user's intent — then confirm once.

### Step 3 — Fetch page content via Notion MCP

For each selected page:

1. Use the Notion MCP **retrieve / fetch page** tool to load page content as
   **Markdown** when the tool supports it; otherwise use the richest text format
   available.
2. Include **child pages** only if the user asked to include subpages or the
   page is clearly a parent index of meeting notes.
3. Do **not** fetch unrelated workspace content beyond the resolved set.

### Step 4 — Write `outputs/notion-input.md`

Overwrite (initial) or append a dated section (update) using this shape:

```markdown
# Notion input capture

## Metadata
- **mode:** initial | update
- **fetched_at:** YYYY-MM-DD
- **search_query:** <string or none>
- **page_count:** <n>

## Page: <Title 1>
- **url:** <canonical Notion URL>
- **page_id:** <id>

<full page content as markdown>

---

## Page: <Title 2>
...
```

**Update mode:** add a new `## Capture YYYY-MM-DD` section at the top (newest first)
instead of deleting prior captures, so **`spec-update`** can see history.

### Step 5 — Handoff summary

Emit a short summary: pages fetched, approximate word count, obvious topics
(discovery, scope, decisions, action items). Flag anything that looks like
**confidential credentials** — do not copy secrets into downstream artifacts.

## Failure modes

| Situation | Action |
|-----------|--------|
| Notion MCP not configured | Point user to README Notion MCP section; stop |
| OAuth / auth error | Ask user to reconnect Notion MCP; stop |
| Page not found / no access | List failing URLs; continue with others if any |
| Empty page body | Note in output; still write metadata |

## Next step

| Mode | Next skill |
|------|------------|
| **initial** | **`spec-normalize-input`** — use `#file:outputs/notion-input.md` as the requirements source |
| **update** | **`spec-update`** — treat this capture as the **new information** input (and merge into `outputs/update-delta.md`) |

## Invocation examples

**Initial run — URLs:**

```text
Use #file:skills/spec-notion-input/SKILL.md

Notion URLs:
- https://www.notion.so/workspace/Product-Discovery-abc123...
- https://www.notion.so/workspace/Stakeholder-Interview-def456...

mode: initial
```

**Initial run — search:**

```text
Use #file:skills/spec-notion-input/SKILL.md

Notion search: "Acme portal discovery meeting"
mode: initial
max_pages: 3
```

**Update run — search + URL:**

```text
Use #file:skills/spec-notion-input/SKILL.md

Notion search: "sprint 12 planning"
Notion URLs:
- https://www.notion.so/workspace/Architecture-review-...

mode: update
```
