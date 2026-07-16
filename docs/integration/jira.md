# Jira Export

## Source
`outputs/stories.md` -- one Jira Story per Story, grouped under Epics.

## Pre-export review (required)

Export is gated by **`spec-full-workflow`** checkpoints:

1. **G — Export preview** — Show epic and story **summary tables** (all items to be created) before any API/MCP calls. See `skills/spec-sync-trackers/SKILL.md` § Export preview.
2. **G2 — Per-story review** — Pause before **each** story; user must `approve`, `skip`, or `edit` before that Jira issue is created.

Optionally persist the preview in `outputs/export-manifest.md`.

## Jira issue structure
- **Issue type:** Epic (for Epics), Story (for Stories)
- **Summary:** `[<ID>] <title>`
- **Description:** user story + acceptance criteria + scenarios (setup/steps/assertions)
- **Story Points:** S=1, M=3, L=5, XL=8
- **Labels:** `spec-workflow`
- **Epic Link:** parent Epic summary

## Via Jira MCP
Use the instructions in `.agent/skills/spec-sync-trackers/skill.md` (Export C).
Create epics once per epic; create stories only after **G2 approve** for that story.

## Manually (CSV import)
After **G** and **G2** approvals, ask your AI assistant:
```
Convert G2-approved stories from outputs/stories.md to a Jira CSV import file.
Columns: Issue Type, Summary, Description, Story Points, Labels, Epic Link
```
Then use Jira -> Projects -> Import issues -> CSV.
