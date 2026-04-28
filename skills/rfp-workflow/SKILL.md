---
name: rfp-workflow
description: End-to-end RFP parsing and Product Requirements Document (PRD) generation workflow. Converts raw RFP text into PRDs, task breakdowns, and user stories.
---

# RFP Workflow

This skill coordinates the full RFP workflow and delegates execution to the
orchestrator skill.

## Execution Trigger

When a user asks to "run the RFP workflow", "process an RFP", or refers to
this repository as a skill, immediately invoke the agentic orchestrator.

## Instructions for the AI Agent

To execute the workflow, read and follow:
`skills/rfp-agentic-orchestrator/SKILL.md`

You should:
1. Treat `skills/rfp-agentic-orchestrator/SKILL.md` as the main entry point.
2. Read the user's provided RFP text or file.
3. Automatically execute all stages (`rfp-ingest` -> `rfp-clarify` ->
   `rfp-prd-draft` -> `rfp-decompose` -> `rfp-stories`) pausing only at the
   defined human-in-the-loop checkpoints.
