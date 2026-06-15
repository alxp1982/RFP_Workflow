# Google Sheets Export

## Source
`outputs/task-breakdown.md` -- the CSV block at the bottom of the file.

## Columns
| Column | Source |
|---|---|
| Type | Epic / Feature / Story / Task |
| ID | E01, F01.01, S01.01.01, T01.01.01.01 |
| Title | item title |
| Parent | parent ID |
| Complexity | S / M / L / XL (Stories only) |
| PRD Trace | FR-/NFR- ID |
| Depends On | Story ID |
| Notes | free text |

## Via MCP
If a Google Sheets MCP is available, use the instructions in
`.agent/skills/spec-sync-trackers/skill.md` (Export A).

## Manually
1. Copy the CSV block from `outputs/task-breakdown.md`.
2. Google Sheets -> File -> Import -> Paste data -> Separator: comma.
3. Freeze row 1, bold headers, color-code by Type.
