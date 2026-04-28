# Architecture

## Approach
Skills-only, no-code pipeline. Each skill is a self-contained markdown prompt
file usable in any AI assistant (GitHub Copilot, Cursor, Claude Code).

Primary execution mode is a single orchestrator skill that runs the full chain
automatically with human-in-the-loop checkpoints.

## Decisions
- CLI-first -> dropped in favour of AI assistant skills (no build required).
- Fixed hierarchy: PRD -> Epic -> Feature -> Story -> Task.
- Clarification stage is mandatory on every input.
- Clarifications are non-blocking. Findings become assumptions.
- Default outputs: local markdown in `outputs/`.
- External exports handled by skill 07 with MCP or manual CSV/JSON.
- Recommended entrypoint: `.agent/skills/rfp-agentic-orchestrator/skill.md`.

## Orchestration checkpoint model
- Checkpoint A: Clarifications review and optional answers.
- Checkpoint B: PRD draft approval/edit.
- Checkpoint C: Decomposition approval/edit.
- Checkpoint D: Export target confirmation.

Only these checkpoints pause execution. All other stages run automatically.

## Pipeline stages

| Stage | Skill | Input | Output |
|---|---|---|---|
| Ingest | rfp-ingest | raw text / file | normalized requirements |
| Clarify | rfp-clarify | normalized reqs | clarifications.md |
| PRD Draft | rfp-prd-draft | reqs + clarifications | prd.md |
| PRD Refine | rfp-prd-refine | prd + answers | prd.md (updated) |
| Decompose | rfp-decompose | prd.md | task-breakdown.md |
| Stories | rfp-stories | task-breakdown.md | stories.md |
| Export | rfp-export | stories + breakdown | tracker items |

## Traceability
- FR/NFR IDs from ingest flow through PRD -> decompose -> stories.
- Every story carries its PRD trace ID.
- Assumptions and open questions propagate through all artifacts.
