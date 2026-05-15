---
name: spec-add-requirement
description: Add or materially change product requirements in spec/ while keeping human-readable markdown and machine-readable YAML (prd.spec.yaml, stories.spec.yaml) aligned, plus digest and changelog.
---

# Add or change requirements (markdown + YAML in sync)

## Purpose

Evolve **`spec/`** when scope or acceptance changes: update **both** narrative markdown
and structured YAML so agents, CI, and importers never drift on IDs or scenarios.

## When to use

- New FR/NFR, revised wording, or removed scope in **`spec/prd.md`**.
- New Story, changed Gherkin, or new acceptance criteria in **`spec/stories.md`**.
- New or re-parented work in **`spec/task-breakdown.md`** (and **`spec/planning-sheet.csv`**
  if you maintain it).
- After edits: refresh **`spec/digest.md`** and append **`spec/CHANGELOG.md`** (see
  **`docs/living-documentation.md`**).

## Prerequisites

- Read **`AGENTS.md`** and skim **`spec/digest.md`**.
- If **`spec/architecture.md`** exists, confirm the change does not silently violate
  **`## Selected stack (locked)`**; if it does, update architecture (or an ADR under
  **`docs/`**) before coding.

## Instructions

1. **Classify the change** — PRD-only, stories-only, or cross-cutting (PRD + stories +
   breakdown). Note whether IDs are **new**, **renamed**, or **retired** (retired ids
   stay in CHANGELOG but should be marked deprecated in YAML where applicable).

2. **Human-readable first** — Edit in order:
   - **`spec/prd.md`** — add/adjust FR/NFR sections; keep `## Assumptions` and
     `## Open Questions` honest.
   - **`spec/stories.md`** — add/adjust stories and Gherkin; preserve **Story ID**
     scheme from **`spec/task-breakdown.md`**.
   - **`spec/task-breakdown.md`** — add Epic/Feature/Story/Task rows as needed; keep
     **Epic → Feature → Story → Task** naming.
   - **`spec/planning-sheet.csv`** — if used, add rows mirroring new hierarchy ids.

3. **Machine-readable sync (required when YAML exists)** — Update in the same session:
   - **`spec/prd.spec.yaml`** — mirror new/updated **FR-** / **NFR-** ids, titles,
     summaries, and `prd_trace`-relevant fields; remove or mark deprecated entries if
     scope was cut (do not orphan ids referenced in stories).
   - **`spec/stories.spec.yaml`** — one story object per Story id in the breakdown;
     align `prd_trace`, `scenarios` (`given` / `when` / `then` lists), and metadata with
     **`spec/stories.md`**.

4. **Digest + changelog** — Update **`spec/digest.md`** (requirement index / epic map
   as needed). Append **`spec/CHANGELOG.md`** with date, short title, bullets listing
   touched ids (FR-/NFR-/S…).

5. **Consistency pass** — Grep YAML for stale ids; ensure every **Story ID** in
   **`stories.spec.yaml`** exists in **`task-breakdown.md`** and **`stories.md`**.

## Outputs checklist

- [ ] `spec/prd.md` updated
- [ ] `spec/prd.spec.yaml` updated (if present)
- [ ] `spec/stories.md` updated (if acceptance changed)
- [ ] `spec/stories.spec.yaml` updated (if present)
- [ ] `spec/task-breakdown.md` / `spec/planning-sheet.csv` updated if backlog changed
- [ ] `spec/digest.md` refreshed
- [ ] `spec/CHANGELOG.md` appended

## ID rules

- **Do not reuse** retired FR/NFR or Story ids for a different meaning.
- New ids must follow the **existing numbering pattern** in each file (extend, do not
  collide).

## Related docs

- **`docs/living-documentation.md`** — how to keep spec and runtime docs current.
- **`docs/engineering-guidelines.md`** — stack guardrails and coding baseline.
