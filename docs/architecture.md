# Architecture

## Approach
Skills-only, no-code pipeline. Each skill is a self-contained markdown prompt
file usable in any AI assistant (GitHub Copilot, Cursor, Claude Code).

Primary execution mode is a single **full workflow** skill that runs the full chain
automatically with human-in-the-loop checkpoints.

## Decisions
- CLI-first -> dropped in favour of AI assistant skills (no build required).
- Fixed hierarchy: PRD -> architecture & stack -> Epic -> Feature -> Story -> Task.
- Clarification stage is mandatory on every input.
- Clarifications are non-blocking. Findings become assumptions.
- Default outputs: local markdown in `outputs/`.
- External exports handled by `spec-sync-trackers` with MCP or manual CSV/JSON.
- Recommended entrypoint: `skills/spec-full-workflow/SKILL.md`.
- Incremental updates: `skills/spec-update/SKILL.md` when `outputs/` already exists.

## Update workflow (incremental)

When new information arrives after an initial run, **`spec-update`**:

1. Reads existing `outputs/` artifacts.
2. Writes `outputs/update-delta.md` as an audit trail.
3. Assesses impact tier (T1 PRD → T4 full downstream).
4. Invokes only affected stage skills (`spec-refine-prd`, architecture, breakdown, stories, repo-kit, sync).
5. Appends to `outputs/spec-changelog.md` (never deletes history).

Checkpoints **U0–U5** gate wide-reaching changes; see `skills/spec-update/SKILL.md`.

## Orchestration checkpoint model
- Checkpoint A: Clarifications review and optional answers.
- Checkpoint B: Infographics model (before PRD draft).
- Checkpoint C: PRD draft approval / edit.
- Checkpoint D: Architecture and technology stack selection (after `spec-architecture-stack`).
- Checkpoint E: Task breakdown approval / edit.
- Checkpoint F: Stories / YAML specs / repo kit authorization.
- Checkpoint G: Export preview — epic and story summary tables before sync.
- Checkpoint G2: Per-story export review (Jira / GitHub — approve, skip, or edit each issue before create).

Only these checkpoints pause execution. All other stages run automatically.

## Pipeline stages

| Stage | Skill | Input | Output |
|---|---|---|---|
| Notion fetch (optional) | spec-notion-input | Notion URLs / search | notion-input.md |
| Normalize | spec-normalize-input | text / file / notion-input.md | normalized requirements |
| Clarify | spec-clarification-pass | normalized reqs | clarifications.md |
| PRD Draft | spec-draft-prd | reqs + clarifications | prd.md |
| PRD Refine | spec-refine-prd | prd + answers | prd.md (updated) |
| Architecture | spec-architecture-stack | prd (+ optional prd.spec.yaml) | architecture.md |
| Decompose | spec-task-breakdown | prd.md + architecture.md | task-breakdown.md |
| Stories | spec-user-stories | task-breakdown.md | stories.md |
| Bootstrap kit | spec-bootstrap-repo | prd, breakdown, stories, … | outputs/repo-kit/ |
| Export / sync | spec-sync-trackers | stories + breakdown | tracker items |
| Update | spec-update | existing outputs + new info | delta merge + refreshed artifacts |

## Traceability
- FR/NFR IDs from the normalize step flow through PRD -> architecture -> task breakdown -> stories.
- Every story carries its PRD trace ID.
- Assumptions and open questions propagate through all artifacts.

## Subagents (optional)

Each pipeline **skill** is a bounded contract: read `SKILL.md`, consume stated inputs,
write defined outputs under `outputs/`. That shape fits **subagent** or **delegated-agent**
patterns in tools that support them (e.g. a parent agent that spawns children with
narrow prompts and merged results).

**Good subagent candidates** (heavy, separable context):
- **`spec-draft-prd`** — large PRD + optional image generation; isolates long context.
- **`spec-architecture-stack`** — cross-cutting technical decisions and stack tradeoffs.
- **`spec-task-breakdown`** — deep hierarchy from full PRD + locked stack; benefits from focused context.
- **`spec-user-stories`** — many stories from breakdown; parallelizable per epic *if* you split inputs (careful with ID consistency).

**Usually keep on the parent** (short, coordination-heavy):
- **`spec-full-workflow`** / **`spec-update`** — owns checkpoints and user dialogue.
- **`spec-normalize-input`** / **`spec-clarification-pass`** — fast; often cheaper to run inline unless you deliberately sandbox parsing.

**If you use subagents**, the **parent** should still: own HITL pauses, pass explicit
file paths or pasted artifacts into each child prompt, require children to respect
templates and `## Assumptions` / `## Open Questions`, and verify handoff files exist
before the next stage. Subagents do not replace checkpoints; they only parallelize
or isolate work **between** them.
