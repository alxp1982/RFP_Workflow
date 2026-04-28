# RFP Workflow - Copilot Instructions

This workspace contains a set of AI skills for analyzing RFPs and producing
delivery artifacts.

Default mode: use the single orchestrator skill for an end-to-end run with
human-in-the-loop checkpoints.

## One-shot agentic mode (recommended)

Use: #file:../.agent/skills/rfp-agentic-orchestrator/skill.md

The orchestrator automatically runs all stages and pauses only at key review
checkpoints (clarifications, PRD, decomposition, export).

## Workflow

1. Ingest requirements: #file:../.agent/skills/rfp-ingest/skill.md
2. Clarify (mandatory, non-blocking): #file:../.agent/skills/rfp-clarify/skill.md
3. Draft PRD: #file:../.agent/skills/rfp-prd-draft/skill.md
4. Refine PRD (if answers available): #file:../.agent/skills/rfp-prd-refine/skill.md
5. Decompose tasks: #file:../.agent/skills/rfp-decompose/skill.md
6. Generate stories: #file:../.agent/skills/rfp-stories/skill.md
7. Export: #file:../.agent/skills/rfp-export/skill.md

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
Use #file:../.agent/skills/rfp-agentic-orchestrator/skill.md

[paste RFP text here]
```
