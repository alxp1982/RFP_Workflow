---
name: rfp-workflow
description: Entry point for this repo. Tells the agent to run the full RFP pipeline via **`rfp-full-workflow`**: normalize → clarify → PRD → backlog → stories → optional sync to trackers, with human checkpoints.
---

# RFP workflow (repo entry)

This skill points to the **full pipeline** skill and does not define a separate
chain.

## Execution Trigger

When a user asks to "run the RFP workflow", "process an RFP", or refers to
this repository as a skill, immediately invoke the **full workflow** skill.

## Instructions for the AI Agent

To execute the workflow, read and follow:
`skills/rfp-full-workflow/SKILL.md`

You should:
1. Treat `skills/rfp-full-workflow/SKILL.md` as the main entry point.
2. Read the user's provided RFP text or file.
3. Start with the **Planning summary** from the full workflow skill (planning-mode style),
   then automatically execute all stages (`rfp-normalize-rfp` -> `rfp-clarification-pass` ->
   `rfp-draft-prd` -> `rfp-task-breakdown` -> `rfp-user-stories`) pausing only at the
   defined human-in-the-loop checkpoints.
