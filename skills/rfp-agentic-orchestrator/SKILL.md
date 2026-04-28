---
name: rfp-agentic-orchestrator
description: Run the full RFP workflow end-to-end (ingest, clarify, PRD draft/refine, decompose, stories, export) with human-in-the-loop checkpoints. Use when the user provides raw RFP text or a file and wants the complete pipeline executed in one invocation.
---

# Skill 00 - Agentic Orchestrator (Human-in-the-Loop)

## Purpose
Run the full RFP workflow end-to-end in a single invocation, while keeping the
human in control at key decision checkpoints.

This skill internally executes:
`rfp-ingest -> rfp-clarify -> rfp-prd-draft -> rfp-prd-refine (if answers provided) -> rfp-decompose -> rfp-stories -> rfp-export`

## Inputs
Provide one of:
- Raw RFP text pasted in chat.
- A source file reference (for example `#file:examples/sample-rfp.md`).

Optional:
- Output targets:
  - PRD: `local-md` (default) | `google-sheets` | other MCP target
  - Stories: `local-md` (default) | `github` | `jira` | other MCP target

## Agentic execution rules
You are an orchestrating product+delivery agent.

1. Execute all stages in order automatically. Do NOT ask the user to manually
   invoke the next skill.
2. Clarifications are mandatory and non-blocking.
3. Keep fixed hierarchy: `Epic -> Feature -> Story -> Task`.
4. Preserve traceability from FR/NFR IDs through decomposition and stories.
5. Every artifact must include `assumptions` and `open_questions`.

## Human-in-the-loop checkpoints
Pause only at these checkpoints:

### Checkpoint A - Clarification review
Show:
- top clarification questions
- working assumptions
- open questions

Ask:
"Do you want to answer any questions now? If yes, provide Q# -> answer. If no, I will continue with assumptions."

### Checkpoint B - PRD review
Show a concise PRD summary (goals, in-scope, out-of-scope, risks).

Ask:
"Approve PRD draft? (approve / edit). If edit, list requested changes."

### Checkpoint C - Plan review
Show decomposition summary (epics count, stories count, major dependencies).

Ask:
"Approve task decomposition? (approve / edit)."

### Checkpoint D - Export confirmation
Show selected export targets and what will be generated.

Ask:
"Confirm export targets and proceed? (yes / change targets)."

*Note: If exporting to GitHub, follow the interactive `gh` CLI export steps defined in `skills/rfp-export/SKILL.md` (checking installation, checking authentication, and confirming project path).*

## Final outputs
Generate and/or update:
- `outputs/clarifications.md`
- `outputs/prd.md`
- `outputs/task-breakdown.md`
- `outputs/planning-sheet.csv`
- `outputs/stories.md`
- optional proposed-solution infographic assets

If export targets are confirmed, run export mapping via `rfp-export`.

## Invocation example
```text
Use #file:skills/rfp-agentic-orchestrator/SKILL.md

Input: [paste RFP text or #file:path]
PRD target: local-md
Stories target: local-md
```
