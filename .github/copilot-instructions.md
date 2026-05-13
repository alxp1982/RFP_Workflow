# RFP Workflow - Copilot Instructions

This workspace contains a set of AI skills for analyzing RFPs and producing
delivery artifacts.

Default mode: use the **full workflow** skill for an end-to-end run with
human-in-the-loop checkpoints.

## One-shot full pipeline (recommended)

Use: #file:../.agent/skills/rfp-full-workflow/skill.md

The full workflow skill automatically runs all stages and pauses only at key review
checkpoints (clarifications, infographic model, PRD, task breakdown, export sync).

## Workflow

1. Normalize requirements: #file:../.agent/skills/rfp-normalize-rfp/skill.md
2. Clarify (mandatory, non-blocking): #file:../.agent/skills/rfp-clarification-pass/skill.md
3. Draft PRD: #file:../.agent/skills/rfp-draft-prd/skill.md
4. Refine PRD (if answers available): #file:../.agent/skills/rfp-refine-prd/skill.md
5. Task breakdown: #file:../.agent/skills/rfp-task-breakdown/skill.md
6. User stories: #file:../.agent/skills/rfp-user-stories/skill.md
7. Sync to trackers: #file:../.agent/skills/rfp-sync-trackers/skill.md

## Defaults
- Clarifications: always run, non-blocking, produce assumptions.
- Hierarchy: PRD -> Epic -> Feature -> Story -> Task (fixed).
- Output: local markdown in `outputs/` by default.
- Every artifact includes `assumptions` and `open_questions` sections.

## Templates
- PRD: #file:../templates/prd.md
- Stories: #file:../templates/stories.md
- Task breakdown: #file:../templates/task-breakdown.md

## Quick start
```
Use #file:../.agent/skills/rfp-full-workflow/skill.md

[paste RFP text here]
```
