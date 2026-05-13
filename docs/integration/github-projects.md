# GitHub Projects Export

## Source
`outputs/stories.md` -- one GitHub Issue per Story.

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
Use the instructions in `.agent/skills/rfp-sync-trackers/skill.md` (Export B).

## Manually
Ask your AI assistant:
```
Convert outputs/stories.md to a list of GitHub issue creation commands
(gh issue create) with appropriate title, body and labels.
```
Then run the generated `gh` commands in your terminal.
