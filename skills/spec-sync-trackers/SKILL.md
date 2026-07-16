---
name: spec-sync-trackers
description: Export generated spec artifacts (task breakdown, planning sheet, stories) to external destinations - Google Sheets, GitHub Projects, or Jira - via the appropriate MCP connector or the gh CLI. Requires checkpoint G (export preview table) and G2 (per-story review) before creating Jira/GitHub issues.
---

# Sync trackers — Sheets, GitHub, Jira

## Purpose
Export generated artifacts to external destinations:
- **Google Sheets** -- task breakdown planning sheet
- **GitHub Projects** -- stories as project items (one issue per story, with G2 review)
- **Jira** -- stories as issues with epics (with G2 review)

## Inputs
- Task breakdown (`#file:outputs/task-breakdown.md`) and Planning sheet (`#file:outputs/planning-sheet.csv`) -- for Sheets.
- Stories (`#file:outputs/stories.md`) -- for GitHub / Jira.
- Export manifest (built at checkpoint **G**; optional file `outputs/export-manifest.md`).

## Export preview (checkpoint G — required for Jira / GitHub)

**Before creating any Jira issue or GitHub issue**, build and show the export
preview. The orchestrator (**`spec-full-workflow`** checkpoint **G**) owns the
human pause; this section defines the **data you must assemble**.

1. Parse **Epics** from `outputs/task-breakdown.md` (type Epic, ids `E*`).
2. Parse **Stories** from `outputs/stories.md` (ids `S*.*.*`), including title,
   user story line, acceptance criteria, scenarios (setup/steps/assertions), complexity, PRD trace, parent epic.
3. Emit two markdown tables (in chat and optionally `outputs/export-manifest.md`):

**Epics to create**

| Epic ID | Title | Stories |
|---------|-------|---------|
| E01 | … | 3 |

**Stories to create**

| Story ID | Epic | Title | Complexity | PRD trace | Status |
|----------|------|-------|------------|-----------|--------|
| S01.01.01 | E01 | … | M | FR-01 | pending |

4. Include header metadata: export target(s), project/repo, timestamp, total counts.

Do **not** call Jira MCP, GitHub MCP, or `gh issue create` until checkpoint **G**
is cleared. If the user removes stories at **G**, update the table before starting **G2**.

## Per-story export review (checkpoint G2 — required for Jira / GitHub)

After **G** is approved, process stories in **Epic ID order, then Story ID order**.

For **each** row with `Status = pending`:

1. Show the **Story export review** card (see **`spec-full-workflow`** checkpoint **G2**).
2. **Wait** for the user: `approve` | `skip` | `edit` (or bulk **approve all remaining**).
3. On **approve** — create **only that story** (and its epic in Jira if not yet created).
4. On **skip** — set `Status = skipped` in the manifest; do not create.
5. On **edit** — update local artifacts if needed, re-show the same story.

Track results and update the manifest **Status** column: `created`, `skipped`, `failed`.

**Jira:** create the Epic once before the first story in that epic; reuse the epic key/link for subsequent stories in the same epic.

**GitHub:** create one issue per approved story; apply labels including epic id.

When finished, report: created count, skipped count, failures, and links/keys where available.

---

## Export A: Google Sheets (task breakdown)

Does **not** use per-story **G2** review. If Sheets is the **only** export target,
checkpoint **G** may be a short confirmation (row count + sheet name) without the
story tables above.

### When using Copilot or Cursor with a Sheets MCP

```
Use the Google Sheets MCP to create a new spreadsheet named
"<project-name> - Task Breakdown".

Sheet 1 - "Planning":
Columns: Type | ID | Title | Parent | Complexity | PRD Trace | Depends On | Notes

Populate from outputs/planning-sheet.csv.
Apply:
- Bold header row
- Color rows by Type: Epic=blue, Feature=green, Story=yellow, Task=white
- Freeze row 1
```

### Without an MCP (manual)
1. Open `outputs/planning-sheet.csv`.
2. Open Google Sheets -> File -> Import -> Upload the CSV file.
3. Apply formatting manually.

---

## Export B: GitHub Projects

**Requires checkpoint G (preview table) and G2 (per-story review) before each `gh issue create` or GitHub MCP create.**

### Interactive Export via `gh` CLI (Recommended)

When exporting to GitHub, you as the AI agent should proactively run an interactive export process:
1. Complete checkpoint **G** (export preview tables) and obtain target repo/project at **G** if not already known.
2. Check if the `gh` CLI is installed (`gh --version`). If not, propose installing it.
3. Check authentication status (`gh auth status`).
   - If NOT authenticated: Ask the user to authenticate by running `gh auth login` in their terminal, and wait for them to confirm.
   - If authenticated: Ask the user to provide or confirm the target GitHub project URL/number and repository owner (if not confirmed at **G**).
4. For **each story** at checkpoint **G2**, after user **approve**:
   - Run `gh issue create` with title `[<Story ID>] <title>` and body per structure below.
   - Use `gh project item-add` to add the issue to the project board when applicable.

### When using Copilot with a GitHub MCP

After **G2 approve** for one story only:

```
Create a GitHub Issue with:
  Title: [<Story ID>] <story title>
  Body:
    ## User Story
    <user story line>

    ## Acceptance Criteria
    <acceptance criteria bullets>

    ## Scenarios
    <setup/steps/assertions block>

    ## Metadata
    PRD Trace: <trace>
    Complexity: <S/M/L/XL>

  Labels: story, <epic-id>
  Project: <project-name>
```

Do not batch-create issues without **G2** approval for each story (unless user said **approve all remaining**).

### Without an MCP (manual)
Generate a JSON import file **only for stories the user approved at G2**:

Ask the AI: "Convert approved stories from outputs/stories.md to a GitHub Issues bulk import JSON
following the format at docs/integration/github-projects.md"

---

## Export C: Jira

**Requires checkpoint G (preview table) and G2 (per-story review) before each Jira MCP create.**

### When using Copilot/Cursor/Claude with a Jira MCP

After **G** and before the first **G2** in an epic, ensure the Epic exists:

```
For each Epic in the export manifest (once per epic, before its first story):
  Create a Jira Epic with summary = [<Epic ID>] <Epic title>.
```

After **G2 approve** for one story only:

```
Create a Jira Story linked to its Epic with:
  Summary: [<Story ID>] <story title>
  Description: user story + acceptance criteria + scenarios (setup/steps/assertions)
  Story Points: S=1, M=3, L=5, XL=8
  Labels: spec-workflow
```

Do not batch-create stories without **G2** approval (unless user said **approve all remaining**).

### Without an MCP (manual)
Ask the AI: "Convert **G2-approved** stories from outputs/stories.md to a Jira CSV import file following
the format at docs/integration/jira.md"

---

## See also
- `docs/integration/google-sheets.md`
- `docs/integration/github-projects.md`
- `docs/integration/jira.md`
- `skills/spec-full-workflow/SKILL.md` — checkpoints **G** and **G2**
