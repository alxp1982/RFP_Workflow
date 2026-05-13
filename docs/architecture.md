# Architecture

## Approach
Skills-only, no-code pipeline. Each skill is a self-contained markdown prompt
file usable in any AI assistant (GitHub Copilot, Cursor, Claude Code).

Primary execution mode is a single **full workflow** skill that runs the full chain
automatically with human-in-the-loop checkpoints.

## Decisions
- CLI-first -> dropped in favour of AI assistant skills (no build required).
- Fixed hierarchy: PRD -> Epic -> Feature -> Story -> Task.
- Clarification stage is mandatory on every input.
- Clarifications are non-blocking. Findings become assumptions.
- Default outputs: local markdown in `outputs/`.
- External exports handled by `rfp-sync-trackers` with MCP or manual CSV/JSON.
- Recommended entrypoint: `.agent/skills/rfp-full-workflow/skill.md`.

## Orchestration checkpoint model
- Checkpoint A: Clarifications review and optional answers.
- Checkpoint B: Infographics model (before PRD draft).
- Checkpoint C: PRD draft approval / edit.
- Checkpoint D: Task breakdown approval / edit.
- Checkpoint E: Export / sync target confirmation.

Only these checkpoints pause execution. All other stages run automatically.

## Pipeline stages

| Stage | Skill | Input | Output |
|---|---|---|---|
| Normalize | rfp-normalize-rfp | raw text / file | normalized requirements |
| Clarify | rfp-clarification-pass | normalized reqs | clarifications.md |
| PRD Draft | rfp-draft-prd | reqs + clarifications | prd.md |
| PRD Refine | rfp-refine-prd | prd + answers | prd.md (updated) |
| Decompose | rfp-task-breakdown | prd.md | task-breakdown.md |
| Stories | rfp-user-stories | task-breakdown.md | stories.md |
| Export / sync | rfp-sync-trackers | stories + breakdown | tracker items |

## Traceability
- FR/NFR IDs from the normalize step flow through PRD -> task breakdown -> stories.
- Every story carries its PRD trace ID.
- Assumptions and open questions propagate through all artifacts.

## Subagents (optional)

Each pipeline **skill** is a bounded contract: read `SKILL.md`, consume stated inputs,
write defined outputs under `outputs/`. That shape fits **subagent** or **delegated-agent**
patterns in tools that support them (e.g. a parent agent that spawns children with
narrow prompts and merged results).

**Good subagent candidates** (heavy, separable context):
- **`rfp-draft-prd`** — large PRD + optional image generation; isolates long context.
- **`rfp-task-breakdown`** — deep hierarchy from full PRD; benefits from focused context.
- **`rfp-user-stories`** — many stories from breakdown; parallelizable per epic *if* you split inputs (careful with ID consistency).

**Usually keep on the parent** (short, coordination-heavy):
- **`rfp-full-workflow`** — owns checkpoints A–E and user dialogue.
- **`rfp-normalize-rfp`** / **`rfp-clarification-pass`** — fast; often cheaper to run inline unless you deliberately sandbox parsing.

**If you use subagents**, the **parent** should still: own HITL pauses, pass explicit
file paths or pasted artifacts into each child prompt, require children to respect
templates and `## Assumptions` / `## Open Questions`, and verify handoff files exist
before the next stage. Subagents do not replace checkpoints; they only parallelize
or isolate work **between** them.
