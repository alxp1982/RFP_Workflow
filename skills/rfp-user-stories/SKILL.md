---
name: rfp-user-stories
description: Generate Gherkin-style acceptance stories (user story, scenario, acceptance criteria) for every Story in the task breakdown, ready for export to GitHub Projects or Jira.
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
