---
name: rfp-export
description: Export generated RFP artifacts (task breakdown, planning sheet, stories) to external destinations - Google Sheets, GitHub Projects, or Jira - via the appropriate MCP connector or the gh CLI.
---

# Skill 07 - Export

## Purpose
Export generated artifacts to external destinations:
- **Google Sheets** -- task breakdown planning sheet
- **GitHub Projects** -- stories as project items
- **Jira** -- stories as issues with epics

## Inputs
- Task breakdown (`#file:outputs/task-breakdown.md`) and Planning sheet (`#file:outputs/planning-sheet.csv`) -- for Sheets.
- Stories (`#file:outputs/stories.md`) -- for GitHub / Jira.

---

## Export A: Google Sheets (task breakdown)

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

### Interactive Export via `gh` CLI (Recommended)

When exporting to GitHub, you as the AI agent should proactively run an interactive export process:
1. Ask the user: "Do you want to export milestones and create tasks directly in a GitHub project?"
2. If the user agrees, check if the `gh` CLI is installed (`gh --version`). If not, propose installing it.
3. Check authentication status (`gh auth status`).
   - If NOT authenticated: Ask the user to authenticate by running `gh auth login` in their terminal, and wait for them to confirm.
   - If authenticated: Ask the user to provide or confirm the target GitHub project URL/number and repository owner.
4. Execute the export using shell commands:
   - For each story, run `gh issue create` (assigning the milestone using `-m` if requested).
   - Use `gh project item-add` to add the created issues to the user's project board.
   - Or use `gh project item-create` to create draft tasks directly if preferred.

### When using Copilot with a GitHub MCP

```
For each story in outputs/stories.md:

Create a GitHub Issue with:
  Title: [<Story ID>] <story title>
  Body:
    ## User Story
    <user story line>

    ## Acceptance Criteria
    <acceptance criteria bullets>

    ## Gherkin
    <gherkin block>

    ## Metadata
    PRD Trace: <trace>
    Complexity: <S/M/L/XL>

  Labels: story, <epic-id>
  Project: <project-name>
```

### Without an MCP (manual)
Generate a JSON import file:

Ask the AI: "Convert outputs/stories.md to a GitHub Issues bulk import JSON
following the format at docs/integration/github-projects.md"

---

## Export C: Jira

### When using Copilot/Cursor/Claude with a Jira MCP

```
For each Epic in outputs/task-breakdown.md:
  Create a Jira Epic with summary = Epic title.

For each Story:
  Create a Jira Story linked to its Epic with:
    Summary: [<Story ID>] <story title>
    Description: user story + acceptance criteria + gherkin
    Story Points: S=1, M=3, L=5, XL=8
    Labels: rfp-workflow
```

### Without an MCP (manual)
Ask the AI: "Convert outputs/stories.md to a Jira CSV import file following
the format at docs/integration/jira.md"

---

## See also
- `docs/integration/google-sheets.md`
- `docs/integration/github-projects.md`
- `docs/integration/jira.md`
