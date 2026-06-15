---
name: spec-update
description: Update existing delivery artifacts when new information arrives after an initial spec run — merge deltas into PRD, architecture, breakdown, stories, YAML specs, digest/changelog, and optionally refresh repo-kit and sync to trackers. Use when `outputs/` already has artifacts and the user provides answers, scope changes, or stakeholder feedback.
---

# Update workflow — merge new information into existing artifacts

## Purpose

Apply **incremental updates** to a spec run that already produced artifacts in
`outputs/`. Typical triggers:

- Clarification answers that were deferred at checkpoint A
- Stakeholder review comments on the PRD or stories
- Scope additions, removals, or priority changes
- New constraints (timeline, compliance, integrations)
- Architecture or stack decisions revised after checkpoint D

This skill **does not** re-run the full pipeline from scratch unless the user
requests a full refresh. It assesses impact, merges deltas, and refreshes only
affected downstream artifacts while preserving FR/NFR/Story traceability IDs.

## Prerequisites

Before starting, confirm these exist (read from disk; do not assume):

| Artifact | Path |
|----------|------|
| PRD | `outputs/prd.md` |
| PRD spec | `outputs/prd.spec.yaml` |
| Spec digest | `outputs/spec-digest.md` |
| Spec changelog | `outputs/spec-changelog.md` |

Optional (determines how far downstream to refresh):

| Artifact | Path |
|----------|------|
| Clarifications | `outputs/clarifications.md` |
| Architecture | `outputs/architecture.md` |
| Task breakdown | `outputs/task-breakdown.md` |
| Planning sheet | `outputs/planning-sheet.csv` |
| Stories | `outputs/stories.md` |
| Stories spec | `outputs/stories.spec.yaml` |
| Repo kit | `outputs/repo-kit/` |

If **`outputs/prd.md`** is missing, stop and tell the user to run
**`spec-full-workflow`** first.

## Inputs

Provide:

1. **New information** — pasted text, bullet list, Q# → answer pairs, review
   comments, or `#file:…` reference.
2. **Scope hint** (optional):
   - `auto` (default) — you assess impact and propose refresh depth
   - `prd-only` — PRD + YAML + digest/changelog only
   - `prd+breakdown` — through task breakdown and planning sheet
   - `full` — through stories, repo-kit, and optional sync
3. **Export targets** (optional) — same as `spec-sync-trackers` when scope includes sync.

## Impact assessment — do this first

Emit an **Update planning summary** (informational; not a hard pause unless
impact is unclear):

### Update planning summary
- **Trigger** — One sentence on what new information was received.
- **Artifacts on disk** — Bullets: which `outputs/` files exist vs missing.
- **Impact tier** — One of:
  - **T1 PRD** — wording, assumptions, FR/NFR edits; no new epics/features
  - **T2 Architecture** — stack, integrations, or NFRs affecting design
  - **T3 Backlog** — new/removed features, story splits, dependency changes
  - **T4 Full downstream** — repo-kit and export need refresh
- **Proposed refresh chain** — Ordered list of stage skills you will invoke
  (see **Refresh map** below).
- **ID policy** — New requirements get **new** FR/NFR ids; existing ids are
  updated in place, never renumbered. New stories get the next free `S*` id in
  their feature. Removed scope is marked `[REMOVED]` in changelog, not deleted
  silently.
- **Checkpoints** — Which human gates apply for this run (see **Checkpoint map**).
- **Next step** — One sentence on what you will do immediately unless the user
  redirects.

Then proceed with execution rules.

## Execution rules

You are an orchestrating product+delivery agent updating an **existing** spec run.

1. **Capture the delta** — Write or append `outputs/update-delta.md` with:
   - date, source (user paste / file / meeting notes)
   - categorized changes: scope, requirements, constraints, decisions, open items
   - mapping to affected FR/NFR/Story ids where known
2. **Merge into clarifications** (if `outputs/clarifications.md` exists) — Move
   resolved items to an `## Applied updates` section; add new open questions.
3. **Refresh PRD** — Follow **`spec-refine-prd`** instructions: overwrite
   `outputs/prd.md`, align **`outputs/prd.spec.yaml`**, regenerate
   **`outputs/spec-digest.md`**, **append** newest-first to
   **`outputs/spec-changelog.md`** (never delete prior log entries).
4. **Downstream refresh** — Invoke only the stages in your proposed chain (see
   **Refresh map**). Each stage skill's own rules apply; pass explicit context
   that this is an **update run** driven by `outputs/update-delta.md`.
5. **Preserve hierarchy** — `Epic -> Feature -> Story -> Task` always.
6. **Traceability** — Every changed FR/NFR must appear in changelog; every new
   or changed Story must reference PRD ids in breakdown and stories specs.
7. **Repo kit** — Re-run **`spec-bootstrap-repo`** only when stories/spec YAML
   changed and the user approves checkpoint F (or scope is `full`).
8. **Export** — Run **`spec-sync-trackers`** only after checkpoint G when
   export was requested.

### Refresh map

| Impact tier | Invoke (in order) |
|-------------|-------------------|
| **T1 PRD** | `spec-refine-prd` (or equivalent merge logic inline) |
| **T2 Architecture** | T1 → **`spec-architecture-stack`** (delta mode: update memo, do not discard locked stack unless user requests) |
| **T3 Backlog** | T1 [→ T2 if needed] → **`spec-task-breakdown`** → **`spec-user-stories`** |
| **T4 Full downstream** | T3 → **`spec-bootstrap-repo`** → [`spec-sync-trackers`] |

For **`spec-architecture-stack`** on an update run: if
`## Selected stack (locked)` exists, treat stack as fixed unless the new
information explicitly requests a stack change; then show options and wait for
checkpoint D before rewriting the locked section.

For **`spec-task-breakdown`** / **`spec-user-stories`**: prefer **surgical**
edits — add rows/tasks/scenarios for new scope, mark removed items
`[REMOVED]` in markdown and changelog, keep stable ids for unchanged work.

## Checkpoint map

Pause and **wait for the user** before destructive or wide-reaching changes:

| After | Checkpoint | Human must clear before you… |
|-------|------------|------------------------------|
| Update planning summary | **U0** (optional) | Proceed if impact tier is T3/T4 or user asked for `auto` with major scope change — confirm proposed refresh chain |
| PRD merge (`spec-refine-prd`) | **U1** | Start architecture refresh (T2+) |
| Architecture delta (if run) | **U2** | Start task breakdown (T3+) |
| Task breakdown refresh | **U3** | Start user stories (T3+) |
| Stories + YAML refresh | **U4** | Run **`spec-bootstrap-repo`** |
| Ready to export | **U5** | Run **`spec-sync-trackers`** (checkpoint **G** preview, then **G2** per story) |

**U0** can be skipped when scope hint is explicit (`prd-only`, etc.) or changes
are clearly minor (typos, assumption wording).

### Checkpoint U0 — Confirm refresh scope

Show impact tier, proposed chain, and id policy.

Ask:
"Proceed with this update plan? (yes / narrow scope / widen scope). To narrow,
say e.g. `prd-only`. To widen, say `full`."

### Checkpoint U1 — PRD review

Show concise diff summary: sections touched, FR/NFR adds/changes/removals,
`[NEW SCOPE]` flags.

Ask:
"Approve PRD updates? (approve / edit). If edit, list sections or FR/NFR ids."

### Checkpoint U2 — Architecture (T2+ only)

Show what changed in `outputs/architecture.md` and whether stack is still locked.

Ask:
"Approve architecture updates? (approve / edit / change stack)."

### Checkpoint U3 — Breakdown (T3+ only)

Show epic/feature/story/task counts and major dependency changes.

Ask:
"Approve task decomposition updates? (approve / edit)."

### Checkpoint U4 — Stories & repo kit (T3+ / full)

Show story count delta and 1–2 example changed Story ids.

Ask:
"Approve story and `stories.spec.yaml` updates, and **authorize refreshing
`outputs/repo-kit/`**? (approve / edit / skip repo-kit)."

### Checkpoint U5 — Export (optional)

Same as checkpoints **G** (export preview — epic/story summary tables) and **G2**
(per-story review before each Jira/GitHub create) in **`spec-full-workflow`**.
Only export stories that are new or changed since the last export unless the user
asks for a full re-export; mark unchanged stories `skipped` in the manifest.

## Final outputs

Update in place (and create if missing):

- `outputs/update-delta.md` — audit trail of incoming information
- `outputs/clarifications.md` — if it existed
- `outputs/prd.md`, `outputs/prd.spec.yaml`
- `outputs/spec-digest.md`, `outputs/spec-changelog.md` (append-only log)
- `outputs/architecture.md` — when T2+
- `outputs/task-breakdown.md`, `outputs/planning-sheet.csv` — when T3+
- `outputs/stories.md`, `outputs/stories.spec.yaml` — when T3+
- `outputs/repo-kit/` — when T4 and checkpoint U4 approved
- Export side effects — when checkpoint U5 confirmed

## Invocation example

```text
Use #file:skills/spec-update/SKILL.md

New information:
- Q3 answer: SSO must use SAML 2.0 with Okta
- Add FR-12: Admin can export audit logs as CSV
- Remove out-of-scope mobile native apps (web responsive only)

Scope: auto
```

## Next step

After a successful update, tell the user which artifacts changed and point to
the newest entry in **`outputs/spec-changelog.md`**. If they copied
`outputs/repo-kit/` to a product repo earlier, remind them to re-copy or
merge the refreshed kit after T4 runs.
