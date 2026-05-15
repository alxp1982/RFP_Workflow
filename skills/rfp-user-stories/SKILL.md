---
name: rfp-user-stories
description: Generate Gherkin-style acceptance stories (user story, scenario, acceptance criteria) for every Story in the task breakdown, plus `stories.spec.yaml` and digest/changelog updates; ready for export to GitHub Projects or Jira.
---

# User stories — Gherkin acceptance criteria

## Purpose
Generate Gherkin-style acceptance stories for every Story in the task
breakdown, ready for export to GitHub Projects or Jira.

## Inputs
- Task breakdown (`#file:outputs/task-breakdown.md`).
- PRD for context (`#file:outputs/prd.md`).

## Instructions

You are a QA lead writing user stories and acceptance criteria.

For each Story in the task breakdown:
1. Write a one-line user story in the format:
   `As a <persona>, I want <action>, so that <outcome>.`
2. Write a Gherkin scenario block (Feature / Scenario / Given / When / Then).
3. Add 2-5 acceptance criteria as a bullet list.
4. Include story metadata for tracker export (see format below).

Rules:
- Persona must match a stakeholder from the PRD.
- Every scenario must be independently testable.
- Include at least one negative/edge-case scenario per Story.
- Keep Gherkin steps concrete and unambiguous.
- Preserve Story ID from task breakdown.

## Structured outputs (required)

In the same step as `outputs/stories.md`, you **must** write:

1. **`outputs/stories.spec.yaml`** — One YAML object per Story in the breakdown.
   **Shape:** `templates/stories.spec.yaml` and **`docs/spec-schema.md`**.
   - `scenarios`: include at least one `kind: happy` and one `kind: edge` per story;
     `given` / `when` / `then` as **lists of short strings** (mirror Gherkin).
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

**Gherkin:**
```gherkin
Feature: <feature title>
  Scenario: <happy path>
    Given <precondition>
    When <action>
    Then <expected outcome>

  Scenario: <edge case>
    Given <precondition>
    When <action>
    Then <expected outcome>
```

**Acceptance Criteria:**
- [ ] <criterion 1>
- [ ] <criterion 2>

---
```

Also produce an export block at the end (see **rfp-sync-trackers** for destinations).

## Next step
Go to **rfp-sync-trackers** to push stories to GitHub Projects, Jira, or Google Sheets.

When running the **full workflow**, **rfp-bootstrap-repo** runs next and builds **`outputs/repo-kit/`** (copy that tree into a new product repository root for spec-driven development).
