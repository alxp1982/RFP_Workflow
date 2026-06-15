---
name: spec-workflow
description: Entry point for this repo. Tells the agent to run the full spec pipeline via **`spec-full-workflow`**, or **`spec-update`** when artifacts already exist — normalize → clarify → PRD → architecture & stack → backlog → stories → repo kit → optional sync, with human checkpoints.
---

# Spec workflow (repo entry)

This skill points to the **full pipeline** and **update** workflow skills; it does
not define a separate chain.

## Execution Trigger

When a user asks to "run the spec workflow", "process requirements", "process an RFP",
or refers to this repository as a skill:

- If **`outputs/prd.md`** (and related artifacts) **already exist** and the user
  provides **new information** → invoke **`spec-update`** (`skills/spec-update/SKILL.md`).
- Otherwise → invoke **`spec-full-workflow`** (`skills/spec-full-workflow/SKILL.md`).

## Instructions for the AI Agent

### Full run (greenfield)

Read and follow: `skills/spec-full-workflow/SKILL.md`

You should:
1. Treat `skills/spec-full-workflow/SKILL.md` as the main entry point.
2. Read the user's provided requirements text or file.
3. Start with the **Planning summary** from the full workflow skill (planning-mode style),
   then automatically execute all stages (`spec-normalize-input` → `spec-clarification-pass` →
   `spec-draft-prd` → `[spec-refine-prd]` → `spec-architecture-stack` → `spec-task-breakdown` →
   `spec-user-stories` → `spec-bootstrap-repo` → `[spec-sync-trackers]`) pausing only at the
   defined human-in-the-loop checkpoints.

### Update run (existing artifacts)

Read and follow: `skills/spec-update/SKILL.md`

Apply new information to existing `outputs/` artifacts; refresh only the affected
downstream stages per the update skill's impact tiers and checkpoints.
