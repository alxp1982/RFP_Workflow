---
name: spec-user-stories
description: Generate structured acceptance stories (user story, scenario, acceptance criteria) for every Story in the task breakdown, plus `stories.spec.yaml` and digest/changelog updates; ready for export to GitHub Projects or Jira.
---

# User stories — structured acceptance criteria

## Purpose
Generate structured acceptance stories for every Story in the task
breakdown, ready for export to GitHub Projects or Jira and directly
consumable by a coding agent (no BDD/Gherkin ceremony to parse).

## Inputs
- Task breakdown (`#file:outputs/task-breakdown.md`).
- PRD for context (`#file:outputs/prd.md`).
- When present, architecture / stack (`#file:outputs/architecture.md`) — use for
  technical wording in scenarios (APIs, auth flows, deployment) without expanding scope
  beyond the PRD.

## Instructions

You are a QA lead writing user stories and acceptance criteria.

For each Story in the task breakdown:
1. Write a one-line user story in the format:
   `As a <persona>, I want <action>, so that <outcome>.`
2. Write one or more scenarios, each with:
   - `setup` — preconditions/state, as short concrete strings.
   - `steps` — ordered actions the actor takes, as short concrete strings.
   - `assertions` — checkable expected outcomes, as short concrete strings.
3. Add 2-5 acceptance criteria as a bullet list.
4. Include story metadata for tracker export (see format below).

Rules:
- Persona must match a stakeholder from the PRD.
- Every scenario must be independently testable.
- Include at least one negative/edge-case scenario per Story.
- Keep `setup`/`steps`/`assertions` concrete and unambiguous — no narrative prose.
- Preserve Story ID from task breakdown.

## Structured outputs (required)

In the same step as `outputs/stories.md`, you **must** write:

1. **`outputs/stories.spec.yaml`** — One YAML object per Story in the breakdown.
   **Shape:** `templates/stories.spec.yaml` and **`docs/spec-schema.md`**.
   - `scenarios`: include at least one `kind: happy` and one `kind: edge` per story;
     `setup` / `steps` / `assertions` as **lists of short strings**.
   - `prd_trace`: list of **FR-** / **NFR-** ids that exist in **`outputs/prd.spec.yaml`**.

2. **`outputs/spec-digest.md`** — Refresh the **Epic → story map** and **Requirement ID index**
   sections using the task breakdown + stories (keep other sections aligned with the PRD).

3. **`outputs/spec-changelog.md`** — Append a **newest-first** entry noting `stories.spec.yaml`
   baseline and any notable traceability batch (e.g. story count).

## Output format

Save as `outputs/stories.md`. Use the template at `templates/stories.md`.

Per story:
```markdown
### Story S01.01.01 - <title>

**User Story:** As a <persona>, I want <action>, so that <outcome>.

**PRD Trace:** FR-03
**Complexity:** M
**Epic:** E01 - <title>

**Scenarios:**

- **<happy path>** (happy)
  - Setup: <precondition>
  - Steps:
    1. <action step>
  - Assertions:
    - <expected outcome>

- **<edge case>** (edge)
  - Setup: <precondition>
  - Steps:
    1. <action step>
  - Assertions:
    - <expected outcome>

**Acceptance Criteria:**
- [ ] <criterion 1>
- [ ] <criterion 2>

---
```

Also produce an export block at the end (see **spec-sync-trackers** for destinations).

## Next step
Go to **spec-sync-trackers** to push stories to GitHub Projects, Jira, or Google Sheets.

When running the **full workflow**, **spec-bootstrap-repo** runs next and builds **`outputs/repo-kit/`** (copy that tree into a new product repository root for spec-driven development).
