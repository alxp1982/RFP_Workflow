# `spec/` — product source of truth

This directory holds the **baseline backlog and PRD** copied from the RFP workflow
run. Treat it as authoritative for **what** to build until intentionally changed.

| File | Role |
|------|------|
| `digest.md` | Short agent-facing summary (from workflow `spec-digest.md` when copied). |
| `CHANGELOG.md` | Append-only spec change log (from workflow `spec-changelog.md` when copied). |
| `prd.spec.yaml` | Machine-readable PRD companion (optional but recommended). |
| `stories.spec.yaml` | Machine-readable stories companion (optional but recommended). |
| `prd.md` | Full product requirements document. |
| `stories.md` | User stories, Gherkin, acceptance criteria, Story IDs. |
| `task-breakdown.md` | Epic → Feature → Story → Task hierarchy and dependencies. |
| `clarifications.md` | Clarification questions and assumptions from intake. |
| `planning-sheet.csv` | Planning / sizing export. |

For day-to-day agent work, prefer **`digest.md`** plus **targeted excerpts** by ID
rather than loading every file in full each turn.
