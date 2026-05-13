---
name: rfp-full-workflow
description: Run the entire RFP-to-delivery pipeline in one go—normalize the RFP, clarification pass, PRD draft and optional refine, task hierarchy, user stories, then sync to trackers—with human checkpoints. Use when the user gives raw RFP text or a file and wants the full chain executed automatically.
---

# Full workflow — RFP to delivery (human checkpoints)

## Purpose
Run the full RFP workflow end-to-end in a single invocation, while keeping the
human in control at key decision checkpoints.

This skill internally executes:
`rfp-normalize-rfp -> rfp-clarification-pass -> rfp-draft-prd -> rfp-refine-prd (if answers provided) -> rfp-task-breakdown -> rfp-user-stories -> rfp-sync-trackers`

## Inputs
Provide one of:
- Raw RFP text pasted in chat.
- A source file reference (for example `#file:examples/sample-rfp.md`).

Optional:
- Output targets:
  - PRD: `local-md` (default) | `google-sheets` | other MCP target
  - Stories: `local-md` (default) | `github` | `jira` | other MCP target

## Execution plan (planning-style summary) — do this first
Before **`rfp-normalize-rfp`**, emit a **Planning summary** for the user: same spirit as
IDE planning mode—short, skimmable, no tool calls required for this block alone.
This step is **informational** (not a human checkpoint); do not wait for approval
unless the user explicitly says to stop or change scope.

Use this structure and headings:

### Planning summary
- **Goal** — One sentence on the delivery outcome this run will pursue from the RFP/input.
- **Inputs understood** — Bullets: source (paste vs file path), rough size or key sections if obvious, and any **PRD / stories / export** targets the user gave (else defaults).
- **Pipeline** — Ordered stages you will run: `rfp-normalize-rfp` → `rfp-clarification-pass` → `rfp-draft-prd` → `[rfp-refine-prd]` → `rfp-task-breakdown` → `rfp-user-stories` → `rfp-sync-trackers`, each with a **few words** on the artifact it produces.
- **Checkpoints** — List gates **A–E** (clarifications, infographic model, PRD, decomposition, export) and when they appear in the run.
- **Initial risks / unknowns** — 2–4 bullets grounded in the RFP preview only (e.g. missing dates, unclear integrations, large scope); do **not** invent client-specific facts.
- **Next step** — One sentence: you will begin **`rfp-normalize-rfp`** immediately after this summary unless the user redirects.

Then proceed with the execution rules below.

## Execution rules
You are an orchestrating product+delivery agent.

0. At kickoff, output the **Planning summary** (section above) once, then run
   the full pipeline in order without asking the user to manually invoke the
   next skill.
1. Clarifications are mandatory and non-blocking.
2. Keep fixed hierarchy: `Epic -> Feature -> Story -> Task`.
3. Preserve traceability from FR/NFR IDs through decomposition and stories.
4. Every artifact must include `assumptions` and `open_questions`.

## Human-in-the-loop checkpoints
Pause only at these checkpoints (the **Planning summary** is not a pause—it is
for alignment only):

### Checkpoint A — Clarifications (questions & assumptions)
Show:
- top clarification questions
- working assumptions
- open questions

Ask:
"Do you want to answer any questions now? If yes, provide Q# -> answer. If no, I will continue with assumptions."

### Checkpoint B — Infographics model (before PRD draft)
Infographics generation (part of `rfp-draft-prd`) requires a highly capable model to succeed and is often skipped by faster models.

Ask:
"The next step (PRD Draft) includes generating infographics. To ensure high-quality visual generation, do you approve switching to or using the most capable model available (e.g., Claude 3.5 Sonnet, GPT-4o, or the best available reasoning/image-generation model) for this step? (yes / no)"

### Checkpoint C — PRD review
Show a concise PRD summary (goals, in-scope, out-of-scope, risks).

Ask:
"Approve PRD draft? (approve / edit). If edit, list requested changes."

### Checkpoint D — Task plan review (breakdown)
Show decomposition summary (epics count, stories count, major dependencies).

Ask:
"Approve task decomposition? (approve / edit)."

### Checkpoint E — Export / sync confirmation
Show selected export targets and what will be generated.

Ask:
"Confirm export targets and proceed? (yes / change targets)."

*Note: If exporting to GitHub, follow the interactive `gh` CLI export steps defined in `skills/rfp-sync-trackers/SKILL.md` (checking installation, checking authentication, and confirming project path).*

## Final outputs
Generate and/or update:
- `outputs/clarifications.md`
- `outputs/prd.md`
- `outputs/task-breakdown.md`
- `outputs/planning-sheet.csv`
- `outputs/stories.md`
- optional proposed-solution infographic assets

If export targets are confirmed, run export mapping via `rfp-sync-trackers`.

## Invocation example
```text
Use #file:skills/rfp-full-workflow/SKILL.md

Input: [paste RFP text or #file:path]
PRD target: local-md
Stories target: local-md
```
