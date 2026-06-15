---
name: spec-full-workflow
description: Run the entire spec-to-delivery pipeline in one go—normalize input, clarification pass, PRD draft and optional refine, architecture and stack selection, task hierarchy, user stories, machine-readable YAML specs (`prd.spec.yaml`, `stories.spec.yaml`) plus digest/changelog, bootstrap a spec-driven repo kit, then sync to trackers—with human checkpoints. Use when the user gives raw requirements text or a file and wants the full chain executed automatically.
---

# Full workflow — requirements to delivery (human checkpoints)

## Purpose
Run the full spec workflow end-to-end in a single invocation, while keeping the
human in control at key decision checkpoints.

This skill internally executes:
`spec-normalize-input -> spec-clarification-pass -> spec-draft-prd -> spec-refine-prd (if answers provided) -> spec-architecture-stack -> spec-task-breakdown -> spec-user-stories -> spec-bootstrap-repo -> spec-sync-trackers`

## Inputs
Provide one of:
- Raw requirements text pasted in chat.
- A source file reference (for example `#file:examples/sample-rfp.md`).

If **`outputs/prd.md`** already exists and the user is adding information rather
than starting fresh, use **`spec-update`** instead of this skill.

Optional:
- Output targets:
  - PRD: `local-md` (default) | `google-sheets` | other MCP target
  - Stories: `local-md` (default) | `github` | `jira` | other MCP target

## Execution plan (planning-style summary) — do this first
Before **`spec-normalize-input`**, emit a **Planning summary** for the user: same spirit as
IDE planning mode—short, skimmable, no tool calls required for this block alone.
This step is **informational** (not a human checkpoint); do not wait for approval
unless the user explicitly says to stop or change scope.

Use this structure and headings:

### Planning summary
- **Goal** — One sentence on the delivery outcome this run will pursue from the RFP/input.
- **Inputs understood** — Bullets: source (paste vs file path), rough size or key sections if obvious, and any **PRD / stories / export** targets the user gave (else defaults).
- **Pipeline** — Ordered stages you will run: `spec-normalize-input` → `spec-clarification-pass` → `spec-draft-prd` → `[spec-refine-prd]` → **`spec-architecture-stack`** → `spec-task-breakdown` → `spec-user-stories` → `spec-bootstrap-repo` → `spec-sync-trackers`, each with a **few words** on the artifact it produces (include **YAML specs + digest/changelog** after PRD and stories).
- **Checkpoints** — **A** clarifications → **B** infographic model → **C** PRD → **D** architecture & stack → **E** decomposition → **F** stories/spec + repo-kit authorization → **G** export preview (epic/story summary table) → **G2** per-story export review (Jira/GitHub). Each gate requires a user reply before the next stage (unless the user explicitly opts out of gates).
- **Initial risks / unknowns** — 2–4 bullets grounded in the RFP preview only (e.g. missing dates, unclear integrations, large scope); do **not** invent client-specific facts.
- **Next step** — One sentence: you will begin **`spec-normalize-input`** immediately after this summary unless the user redirects.

Then proceed with the execution rules below.

## Execution rules
You are an orchestrating product+delivery agent.

0. At kickoff, output the **Planning summary** (section above) once. Then advance
   the pipeline **one stage at a time**, invoking the next skill yourself **only after**
   the human clears the **checkpoint** that guards that stage (see **Checkpoint map**
   below). **Do not** “fast forward” past a checkpoint in a single assistant turn unless
   the user explicitly instructs you to (e.g. “approve all checkpoints and run end-to-end”).
1. Clarifications are mandatory: you always run **`spec-clarification-pass`** and write
   `outputs/clarifications.md`. **Checkpoint A** is still required: present questions and
   assumptions and **wait** for the user to answer or decline; if they decline, continue
   with stated assumptions before **`spec-draft-prd`**.
2. Keep fixed hierarchy: `Epic -> Feature -> Story -> Task`.
3. Preserve traceability from FR/NFR IDs through decomposition and stories.
4. Every artifact must include `assumptions` and `open_questions`.
5. After **`spec-user-stories`** **and** **checkpoint F**, run **`spec-bootstrap-repo`**
   (see `skills/spec-bootstrap-repo/SKILL.md`) so `outputs/repo-kit/` is ready to copy
   into a new product repo **before** **`spec-sync-trackers`**.

### Checkpoint map (what waits for whom)

| After skill(s) | Checkpoint | Human must clear before you… |
|----------------|------------|------------------------------|
| `spec-normalize-input` + `spec-clarification-pass` | **A** | Start **`spec-draft-prd`** (and infographics per **B**) |
| (just before heavy PRD draft / infographics) | **B** | Proceed with infographic generation inside draft PRD |
| `spec-draft-prd` [+ optional `spec-refine-prd`] | **C** | Start **`spec-architecture-stack`** |
| `spec-architecture-stack` | **D** | Update **`outputs/architecture.md`** with the chosen stack (see checkpoint text), then start **`spec-task-breakdown`** |
| `spec-task-breakdown` | **E** | Start **`spec-user-stories`** |
| `spec-user-stories` (incl. `stories.spec.yaml`, digest refresh) | **F** | Run **`spec-bootstrap-repo`** (writes `outputs/repo-kit/`) |
| (ready to export) | **G** | Start **`spec-sync-trackers`** (after export preview table is approved) |
| (each story/issue, Jira or GitHub only) | **G2** | Create that story in the target tracker |

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
Infographics generation (part of `spec-draft-prd`) requires a highly capable model to succeed and is often skipped by faster models.

Ask:
"The next step (PRD Draft) includes generating infographics. To ensure high-quality visual generation, do you approve switching to or using the most capable model available (e.g., Claude 3.5 Sonnet, GPT-4o, or the best available reasoning/image-generation model) for this step? (yes / no)"

### Checkpoint C — PRD review
Show a concise PRD summary (goals, in-scope, out-of-scope, risks).

Ask:
"Approve PRD draft? (approve / edit). If edit, list requested changes."

### Checkpoint D — Architecture and technology stack
Show:
- one-paragraph architecture summary
- stack options table (or link to headings in `outputs/architecture.md`)
- your recommendation line

Ask:
"Which stack option do you adopt for implementation planning? (option name / letter, or describe a hybrid). I will lock **`outputs/architecture.md`** under **`## Selected stack (locked)`** accordingly."

After the user answers, **edit `outputs/architecture.md`**: replace **`## Selected stack (pending)`** with **`## Selected stack (locked)`**, fill the chosen components and date, and keep comparison/recommendation sections unless the user asks to trim them.

### Checkpoint E — Task plan review (breakdown)
Show decomposition summary (epics count, stories count, major dependencies).

Ask:
"Approve task decomposition? (approve / edit)."

### Checkpoint F — Stories, YAML specs, and repo kit
Show (after `outputs/stories.md` and `outputs/stories.spec.yaml` are written):
- story count and 1–2 example Story IDs
- one-line confirmation that digest/changelog were updated for stories if applicable

Ask:
"Approve stories and machine-readable `stories.spec.yaml` (and digest updates), and **authorize generating `outputs/repo-kit/`** for a fresh product repo? (approve / edit). If edit, list Story IDs or sections to change."

**Do not** run **`spec-bootstrap-repo`** until the user approves here. Copying into
`outputs/repo-kit/` is **not** an export to Jira/GitHub—it materializes a portable
tree for a **new** codebase repo and should only happen after explicit approval of
stories/specs (or a user instruction to skip this gate).

### Checkpoint G — Export preview (summary table)

Applies when export targets include **Jira** and/or **GitHub** (Google Sheets
uses the planning sheet only; see **`spec-sync-trackers`** Export A).

Before invoking **`spec-sync-trackers`**, build the export manifest from
`outputs/task-breakdown.md`, `outputs/planning-sheet.csv`, and
`outputs/stories.md` (see **`spec-sync-trackers`** § Export preview).

Show:

1. **Export targets** — Jira project / GitHub repo+project (or “not configured yet”).
2. **Epics to create** (Jira/GitHub) — summary table:

| Epic ID | Title | Stories |
|---------|-------|---------|

3. **Stories to create** — full summary table (every story that will be exported):

| Story ID | Epic | Title | Complexity | PRD trace | Status |
|----------|------|-------|------------|-----------|--------|

Use `Status = pending` for all rows initially.

4. **Counts** — epics, stories, skipped (0 until G2), created (0 until export runs).

Optionally write the same tables to **`outputs/export-manifest.md`** for audit.

Ask:
"Approve this export plan and proceed to per-story review? (approve / edit / cancel).
To edit, list Story IDs to remove, retitle, or reassign before export.
Say **approve all stories** only if you want to skip individual G2 pauses (not recommended for first run)."

**Do not** create any Jira issues or GitHub issues until **G** is cleared (and
each **G2** unless the user opted into bulk approve).

### Checkpoint G2 — Per-story export review (Jira / GitHub)

After **G** is approved, **`spec-sync-trackers`** walks stories **in Epic ID
then Story ID order**. For **each** story slated for export, **pause** and show:

```markdown
#### Story export review: <Story ID> — <title>
- **Epic:** <Epic ID> — <epic title>
- **User story:** <one line>
- **Acceptance criteria:** <bullets or count + first 2>
- **Complexity / points:** <S/M/L/XL> (Jira points if applicable)
- **PRD trace:** <FR-/NFR- ids>
- **Target:** Jira | GitHub
```

Ask:
"Create this issue? (approve / skip / edit). If edit, describe changes; update
`outputs/stories.md` if needed, then re-show this card."

Rules:
- **approve** — create exactly one issue for this story, then move to the next G2.
- **skip** — mark `Status = skipped` in the manifest table; do not create; continue.
- **edit** — apply edits, re-show the same story; do not advance until approved or skipped.
- If the user says **approve all remaining** at any G2, you may create subsequent
  stories without further G2 pauses, but still report a final created/skipped summary.

After all stories are processed, show a **Export complete** summary: created,
skipped, failed (with links/keys if the MCP or `gh` CLI returned them).

*Note: Google Sheets export (planning sheet) does not use G2 — only checkpoint **G**
if Sheets is the sole target, or run Sheets after Jira/GitHub story export completes.*

*Note: If exporting to GitHub, follow the interactive `gh` CLI export steps defined in `skills/spec-sync-trackers/SKILL.md` (checking installation, checking authentication, and confirming project path).*

## Final outputs
Generate and/or update:
- `outputs/clarifications.md`
- `outputs/prd.md`
- `outputs/prd.spec.yaml`
- `outputs/spec-digest.md`
- `outputs/spec-changelog.md`
- `outputs/architecture.md`
- `outputs/task-breakdown.md`
- `outputs/planning-sheet.csv`
- `outputs/stories.md`
- `outputs/stories.spec.yaml`
- `outputs/repo-kit/` — portable **new-repo bootstrap** (`spec/`, `AGENTS.md`, `CLAUDE.md`, `.cursor/`, `.claude/`, `.github/copilot-instructions.md`); see **`spec-bootstrap-repo`**
- optional proposed-solution infographic assets

If export targets are confirmed, run export mapping via `spec-sync-trackers`.

## Invocation example
```text
Use #file:skills/spec-full-workflow/SKILL.md

Input: [paste RFP text or #file:path]
PRD target: local-md
Stories target: local-md
```
