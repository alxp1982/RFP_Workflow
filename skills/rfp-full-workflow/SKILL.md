---
name: rfp-full-workflow
description: Run the entire RFP-to-delivery pipeline in one go—normalize the RFP, clarification pass, PRD draft and optional refine, task hierarchy, user stories, machine-readable YAML specs (`prd.spec.yaml`, `stories.spec.yaml`) plus digest/changelog, bootstrap a spec-driven repo kit, then sync to trackers—with human checkpoints. Use when the user gives raw RFP text or a file and wants the full chain executed automatically.
---

# Full workflow — RFP to delivery (human checkpoints)

## Purpose
Run the full RFP workflow end-to-end in a single invocation, while keeping the
human in control at key decision checkpoints.

This skill internally executes:
`rfp-normalize-rfp -> rfp-clarification-pass -> rfp-draft-prd -> rfp-refine-prd (if answers provided) -> rfp-task-breakdown -> rfp-user-stories -> rfp-bootstrap-repo -> rfp-sync-trackers`

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
- **Pipeline** — Ordered stages you will run: `rfp-normalize-rfp` → `rfp-clarification-pass` → `rfp-draft-prd` → `[rfp-refine-prd]` → `rfp-task-breakdown` → `rfp-user-stories` → `rfp-bootstrap-repo` → `rfp-sync-trackers`, each with a **few words** on the artifact it produces (include **YAML specs + digest/changelog** after PRD and stories).
- **Checkpoints** — **A** clarifications → **B** infographic model → **C** PRD → **D** decomposition → **F** stories/spec + repo-kit authorization → **E** export/sync. Each gate requires a user reply before the next stage (unless the user explicitly opts out of gates).
- **Initial risks / unknowns** — 2–4 bullets grounded in the RFP preview only (e.g. missing dates, unclear integrations, large scope); do **not** invent client-specific facts.
- **Next step** — One sentence: you will begin **`rfp-normalize-rfp`** immediately after this summary unless the user redirects.

Then proceed with the execution rules below.

## Execution rules
You are an orchestrating product+delivery agent.

0. At kickoff, output the **Planning summary** (section above) once. Then advance
   the pipeline **one stage at a time**, invoking the next skill yourself **only after**
   the human clears the **checkpoint** that guards that stage (see **Checkpoint map**
   below). **Do not** “fast forward” past a checkpoint in a single assistant turn unless
   the user explicitly instructs you to (e.g. “approve all checkpoints and run end-to-end”).
1. Clarifications are mandatory: you always run **`rfp-clarification-pass`** and write
   `outputs/clarifications.md`. **Checkpoint A** is still required: present questions and
   assumptions and **wait** for the user to answer or decline; if they decline, continue
   with stated assumptions before **`rfp-draft-prd`**.
2. Keep fixed hierarchy: `Epic -> Feature -> Story -> Task`.
3. Preserve traceability from FR/NFR IDs through decomposition and stories.
4. Every artifact must include `assumptions` and `open_questions`.
5. After **`rfp-user-stories`** **and** **checkpoint F**, run **`rfp-bootstrap-repo`**
   (see `skills/rfp-bootstrap-repo/SKILL.md`) so `outputs/repo-kit/` is ready to copy
   into a new product repo **before** **`rfp-sync-trackers`**.

### Checkpoint map (what waits for whom)

| After skill(s) | Checkpoint | Human must clear before you… |
|----------------|------------|------------------------------|
| `rfp-normalize-rfp` + `rfp-clarification-pass` | **A** | Start **`rfp-draft-prd`** (and infographics per **B**) |
| (just before heavy PRD draft / infographics) | **B** | Proceed with infographic generation inside draft PRD |
| `rfp-draft-prd` [+ optional `rfp-refine-prd`] | **C** | Start **`rfp-task-breakdown`** |
| `rfp-task-breakdown` | **D** | Start **`rfp-user-stories`** |
| `rfp-user-stories` (incl. `stories.spec.yaml`, digest refresh) | **F** | Run **`rfp-bootstrap-repo`** (writes `outputs/repo-kit/`) |
| (ready to export) | **E** | Run **`rfp-sync-trackers`** |

## Human-in-the-loop checkpoints
Pause at each checkpoint below and **wait for the user’s reply** before continuing
(the **Planning summary** is not a pause—it is for alignment only):

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

### Checkpoint F — Stories, YAML specs, and repo kit
Show (after `outputs/stories.md` and `outputs/stories.spec.yaml` are written):
- story count and 1–2 example Story IDs
- one-line confirmation that digest/changelog were updated for stories if applicable

Ask:
"Approve stories and machine-readable `stories.spec.yaml` (and digest updates), and **authorize generating `outputs/repo-kit/`** for a fresh product repo? (approve / edit). If edit, list Story IDs or sections to change."

**Do not** run **`rfp-bootstrap-repo`** until the user approves here. Copying into
`outputs/repo-kit/` is **not** an export to Jira/GitHub—it materializes a portable
tree for a **new** codebase repo and should only happen after explicit approval of
stories/specs (or a user instruction to skip this gate).

### Checkpoint E — Export / sync confirmation
Show selected export targets and what will be generated.

Ask:
"Confirm export targets and proceed? (yes / change targets)."

*Note: If exporting to GitHub, follow the interactive `gh` CLI export steps defined in `skills/rfp-sync-trackers/SKILL.md` (checking installation, checking authentication, and confirming project path).*

## Final outputs
Generate and/or update:
- `outputs/clarifications.md`
- `outputs/prd.md`
- `outputs/prd.spec.yaml`
- `outputs/spec-digest.md`
- `outputs/spec-changelog.md`
- `outputs/task-breakdown.md`
- `outputs/planning-sheet.csv`
- `outputs/stories.md`
- `outputs/stories.spec.yaml`
- `outputs/repo-kit/` — portable **new-repo bootstrap** (`spec/`, `AGENTS.md`, `CLAUDE.md`, `.cursor/`, `.claude/`, `.github/copilot-instructions.md`); see **`rfp-bootstrap-repo`**
- optional proposed-solution infographic assets

If export targets are confirmed, run export mapping via `rfp-sync-trackers`.

## Invocation example
```text
Use #file:skills/rfp-full-workflow/SKILL.md

Input: [paste RFP text or #file:path]
PRD target: local-md
Stories target: local-md
```
