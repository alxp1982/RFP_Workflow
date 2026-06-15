# Spec Workflow - Copilot Instructions

This workspace contains a set of AI skills for turning requirements input into
delivery artifacts.

Default mode: use the **full workflow** skill for an end-to-end run with
human-in-the-loop checkpoints.

When `outputs/` already has artifacts and the user provides **new information later**,
use the **update workflow** skill instead.

## One-shot full pipeline (recommended)

Use: #file:../.agent/skills/spec-full-workflow/skill.md

The full workflow skill automatically runs all stages and pauses only at key review
checkpoints (clarifications, infographic model, PRD, architecture & stack, task breakdown, stories/repo kit, **export preview G**, **per-story export G2** for Jira/GitHub).

## Update existing artifacts

Use: #file:../.agent/skills/spec-update/skill.md

Provide the new information (answers, scope changes, stakeholder feedback) and optionally
which artifacts to refresh. The update workflow merges deltas and keeps YAML specs,
digest, and changelog aligned.

## Workflow

1. Normalize requirements: #file:../.agent/skills/spec-normalize-input/skill.md
2. Clarify (mandatory, non-blocking): #file:../.agent/skills/spec-clarification-pass/skill.md
3. Draft PRD: #file:../.agent/skills/spec-draft-prd/skill.md
4. Refine PRD (if answers available): #file:../.agent/skills/spec-refine-prd/skill.md
5. Architecture & stack options: #file:../skills/spec-architecture-stack/SKILL.md
6. Task breakdown: #file:../.agent/skills/spec-task-breakdown/skill.md
7. User stories: #file:../.agent/skills/spec-user-stories/skill.md
8. Bootstrap product repo kit (`outputs/repo-kit/`): #file:../skills/spec-bootstrap-repo/SKILL.md
9. Sync to trackers: #file:../.agent/skills/spec-sync-trackers/skill.md

## Defaults
- Clarifications: always run on initial full runs, non-blocking, produce assumptions.
- Hierarchy: PRD -> architecture & stack -> Epic -> Feature -> Story -> Task (fixed).
- Output: local markdown and YAML in `outputs/` by default (`prd.spec.yaml`, `stories.spec.yaml`, `spec-digest.md`, `spec-changelog.md`; see `docs/spec-schema.md`).
- Every artifact includes `assumptions` and `open_questions` sections.

## Templates
- PRD: #file:../templates/prd.md
- Stories: #file:../templates/stories.md
- Task breakdown: #file:../templates/task-breakdown.md
- Architecture memo: #file:../templates/architecture.md
- PRD YAML skeleton: #file:../templates/prd.spec.yaml
- Stories YAML skeleton: #file:../templates/stories.spec.yaml
- Spec digest / changelog headings: #file:../templates/spec-digest.md · #file:../templates/spec-changelog.md
- Schema reference: #file:../docs/spec-schema.md
- New product repo kit (spec-driven scaffold): #file:../templates/repo-kit/README.md (full tree under `templates/repo-kit/`)

## Quick start
```
Use #file:../.agent/skills/spec-full-workflow/skill.md

[paste requirements text here]
```

## Update quick start
```
Use #file:../.agent/skills/spec-update/skill.md

New information: [paste answers, scope changes, or stakeholder feedback]
Scope: auto | prd-only | prd+breakdown | full
```
