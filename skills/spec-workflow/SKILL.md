---
name: spec-workflow
description: Entry point for this repo. Tells the agent to run the full spec pipeline via **`spec-full-workflow`**, or **`spec-update`** when artifacts already exist — optional Notion meeting notes via MCP, normalize → clarify → PRD → architecture & stack → backlog → stories → repo kit → optional sync, with human checkpoints.
---

# Spec workflow (repo entry)

This skill points to the **full pipeline** and **update** workflow skills; it does
not define a separate chain.

## Execution Trigger

When a user asks to "run the spec workflow", "process requirements", "process an RFP",
refers to **Notion meeting notes**, or refers to this repository as a skill:

- If **`outputs/prd.md`** (and related artifacts) **already exist** and the user
  provides **new information** (paste, file, or **Notion URLs/search**) → invoke
  **`spec-update`** (`skills/spec-update/SKILL.md`).
- Otherwise → invoke **`spec-full-workflow`** (`skills/spec-full-workflow/SKILL.md`).

## Notion meeting notes

When the user provides **Notion page URL(s)** and/or a **search string**, the
orchestrator runs **`spec-notion-input`** first (requires Notion MCP — see README).
Do not skip the fetch and paste from memory.

## Instructions for the AI Agent

### Full run (greenfield)

Read and follow: `skills/spec-full-workflow/SKILL.md`

You should:
1. Treat `skills/spec-full-workflow/SKILL.md` as the main entry point.
2. Read the user's provided requirements text, file, or Notion parameters.
3. Start with the **Planning summary** from the full workflow skill (planning-mode style),
   then automatically execute all stages (`[spec-notion-input]` → `spec-normalize-input` →
   `spec-clarification-pass` → `spec-draft-prd` → `[spec-refine-prd]` →
   `spec-architecture-stack` → `spec-task-breakdown` → `spec-user-stories` →
   `spec-bootstrap-repo` → `[spec-sync-trackers]`) pausing only at the defined
   human-in-the-loop checkpoints.

### Update run (existing artifacts)

Read and follow: `skills/spec-update/SKILL.md`

Apply new information to existing `outputs/` artifacts; when Notion input is given,
run **`spec-notion-input`** (`mode: update`) before the impact assessment.
