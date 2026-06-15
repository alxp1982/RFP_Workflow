# GitHub Projects Export

## Source
`outputs/stories.md` -- one GitHub Issue per Story.

## Pre-export review (required)

Export is gated by **`spec-full-workflow`** checkpoints:

1. **G — Export preview** — Show epic and story **summary tables** (all items to be created) before any API/MCP/`gh` calls. See `skills/spec-sync-trackers/SKILL.md` § Export preview.
2. **G2 — Per-story review** — Pause before **each** story; user must `approve`, `skip`, or `edit` before that GitHub issue is created.

Optionally persist the preview in `outputs/export-manifest.md`.

## Issue structure
- **Title:** `[<Story ID>] <story title>`
- **Body:**
  - User Story line
  - Acceptance Criteria (checkboxes)
  - Gherkin block
  - Metadata (PRD trace, complexity, epic)
- **Labels:** `story`, `<epic-id>`
- **Project:** target GitHub Project board

## Via GitHub MCP
Use the instructions in `.agent/skills/spec-sync-trackers/skill.md` (Export B).
Create issues only after **G2 approve** for that story.

## Manually
After **G** and **G2** approvals, ask your AI assistant:
```
Convert G2-approved stories from outputs/stories.md to a list of GitHub issue creation commands
(gh issue create) with appropriate title, body and labels.
```
Then run the generated `gh` commands in your terminal.
