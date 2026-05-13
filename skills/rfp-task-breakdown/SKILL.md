---
name: rfp-task-breakdown
description: Decompose a finalized PRD into a hierarchical technical implementation plan using the fixed hierarchy Epic -> Feature -> Story -> Task, with complexity estimates, dependencies, and PRD traceability.
---

# Task breakdown — Epic → Feature → Story → Task

## Purpose
Decompose the PRD into a detailed, hierarchical technical implementation plan
using the fixed hierarchy:

  Epic -> Feature -> Story -> Task

## Inputs
- Final PRD (`#file:outputs/prd.md`).

## Instructions

You are a technical lead decomposing product requirements into actionable
engineering work.

Rules:
1. Use ONLY the fixed hierarchy: Epic > Feature > Story > Task.
2. Every story must be independently deliverable and testable.
3. Every story must trace back to at least one FR/NFR ID from the PRD.
4. Every task must be concrete (< 1 day of work). No vague tasks.
5. Include a complexity estimate for each Story: S / M / L / XL.
6. Include a dependency reference where a Story depends on another Story.
7. Flag any technical assumptions made during decomposition.
8. The hierarchy must be complete enough to populate a planning spreadsheet.

## Output format

Save the markdown hierarchy as `outputs/task-breakdown.md`. Use the template at
`templates/task-breakdown.md`.

Structure:
```
Epic E01: <title>
  Feature F01.01: <title>
    Story S01.01.01 [M] (traces: FR-03): <title>
      Task T01.01.01.01: <concrete action>
      Task T01.01.01.02: <concrete action>
    Story S01.01.02 [S] (traces: NFR-01): <title>
      Task T01.01.02.01: <concrete action>
```

Also produce a separate CSV file for Google Sheets/Excel import:
Save as `outputs/planning-sheet.csv` (or `.xlsx` if your tools support it natively).
If generating CSV, use the template at `templates/planning-sheet.csv`:

```csv
Type,ID,Title,Parent,Complexity,PRD Trace,Depends On,Notes
Epic,E01,...
Feature,F01.01,...,E01,...
Story,S01.01.01,...,F01.01,M,FR-03,...
Task,T01.01.01.01,...,S01.01.01,...
```

## Next step
Go to **rfp-user-stories**.
