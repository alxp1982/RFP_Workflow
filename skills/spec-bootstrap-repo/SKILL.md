---
name: spec-bootstrap-repo
description: After PRD, breakdown, and stories exist, emit outputs/repo-kit/ — a self-contained tree (AGENTS.md, spec/, and Cursor / Claude Code / GitHub Copilot hooks) ready to copy into a fresh product repository for AI spec-driven development.
---

# Bootstrap repo kit — spec-driven product repo

## Purpose

Materialize **`outputs/repo-kit/`**: a **portable folder** the user can copy to the
**root of a new git repository** so the codebase starts with:

**Important:** Everything under **`templates/repo-kit/`** (including nested `.cursor/`,
`.claude/`, `docs/`, and any `SKILL.md` files there) is **scaffolding for the destination
product repository only**. Those paths are **not** Spec Workflow pipeline skills in
this repo and are **not** meant to be run from `skills/` here—they are copied into
`outputs/repo-kit/` so the **new** product repo has its own agent rules and skills.

- **`spec/`** — PRD, stories, task breakdown, clarifications, planning sheet (baseline backlog), architecture/stack decision when produced upstream, plus **`prd.spec.yaml`** / **`stories.spec.yaml`** when produced upstream.
- **`spec/digest.md`** — short default agent context (regenerate when the PRD changes a lot).
- **`spec/CHANGELOG.md`** — append-only spec change log (seed with an initial baseline entry).
- **`AGENTS.md`** — cross-tool agent instructions for this product.
- **`CLAUDE.md`** — Claude Code root entry (placeholders); points to `AGENTS.md` and `spec/`.
- **`.github/copilot-instructions.md`** — GitHub Copilot repository instructions.
- **`.cursor/rules/spec-driven-product.mdc`** — Cursor always-on guidance tied to `spec/`.
- **`.cursor/rules/engineering-guardrails.mdc`** — Cursor: stack guardrails and baseline coding expectations.
- **`.cursor/skills/project-spec-context/`** — Cursor skill to load digest + slices by Story ID.
- **`.cursor/skills/spec-add-requirement/`** — Cursor skill: add requirements with markdown + YAML sync.
- **`.claude/skills/project-spec-context/`** — Claude Code skill (same workflow as the Cursor skill).
- **`.claude/skills/spec-add-requirement/`** — Claude Code skill (same workflow as Cursor **spec-add-requirement**).
- **`docs/living-documentation.md`** — keeping spec and runtime docs current during development.
- **`docs/engineering-guidelines.md`** — architecture guardrails and baseline coding guidelines.
- **`.gitignore`** — generic baseline for a polyglot app repo.

This step **does not** replace `outputs/prd.md` etc. It **copies** them into the kit
so `repo-kit/` is self-contained after copy.

## When to run

- **Automatically** as part of **`spec-full-workflow`** only **after checkpoint F**
  (stories/spec approval and explicit authorization to materialize the repo kit), and
  **before** **`spec-sync-trackers`**.
- May also be invoked alone when the user asks to “refresh the repo kit” after edits
  to `outputs/prd.md` / `outputs/architecture.md` / stories / breakdown.

## Inputs

Read from this spec workflow workspace:

- `outputs/prd.md`
- `outputs/stories.md`
- `outputs/task-breakdown.md`
- `outputs/clarifications.md`
- `outputs/planning-sheet.csv` (if missing, note in kit README and skip copy)
- `outputs/architecture.md` (if present — copy into kit `spec/`)
- When present (required by upstream skills): **`outputs/prd.spec.yaml`**,
  **`outputs/stories.spec.yaml`**, **`outputs/spec-digest.md`**, **`outputs/spec-changelog.md`**
- Templates under `templates/repo-kit/` (see layout below)

## Outputs (write these paths)

Create or overwrite:

| Output path | Source |
|-------------|--------|
| `outputs/repo-kit/README.md` | `templates/repo-kit/README.md` with placeholders replaced |
| `outputs/repo-kit/AGENTS.md` | `templates/repo-kit/AGENTS.md` with placeholders replaced |
| `outputs/repo-kit/CLAUDE.md` | `templates/repo-kit/CLAUDE.md` with placeholders replaced |
| `outputs/repo-kit/.gitignore` | `templates/repo-kit/gitignore` (rename to dotfile) |
| `outputs/repo-kit/.github/copilot-instructions.md` | Copy of `templates/repo-kit/.github/copilot-instructions.md` |
| `outputs/repo-kit/.cursor/rules/spec-driven-product.mdc` | Copy of `templates/repo-kit/.cursor/rules/spec-driven-product.mdc` |
| `outputs/repo-kit/.cursor/rules/engineering-guardrails.mdc` | Copy of `templates/repo-kit/.cursor/rules/engineering-guardrails.mdc` |
| `outputs/repo-kit/.cursor/skills/project-spec-context/SKILL.md` | Copy of `templates/repo-kit/.cursor/skills/project-spec-context/SKILL.md` |
| `outputs/repo-kit/.cursor/skills/spec-add-requirement/SKILL.md` | Copy of `templates/repo-kit/.cursor/skills/spec-add-requirement/SKILL.md` |
| `outputs/repo-kit/.claude/skills/project-spec-context/SKILL.md` | Copy of `templates/repo-kit/.claude/skills/project-spec-context/SKILL.md` |
| `outputs/repo-kit/.claude/skills/spec-add-requirement/SKILL.md` | Copy of `templates/repo-kit/.claude/skills/spec-add-requirement/SKILL.md` |
| `outputs/repo-kit/docs/living-documentation.md` | Copy of `templates/repo-kit/docs/living-documentation.md` |
| `outputs/repo-kit/docs/engineering-guidelines.md` | Copy of `templates/repo-kit/docs/engineering-guidelines.md` |
| `outputs/repo-kit/spec/README.md` | Copy of `templates/repo-kit/spec/README.md` |
| `outputs/repo-kit/spec/architecture.md` | **Full copy** of `outputs/architecture.md` if it exists |
| `outputs/repo-kit/spec/prd.md` | **Full copy** of `outputs/prd.md` |
| `outputs/repo-kit/spec/stories.md` | **Full copy** of `outputs/stories.md` |
| `outputs/repo-kit/spec/task-breakdown.md` | **Full copy** of `outputs/task-breakdown.md` |
| `outputs/repo-kit/spec/clarifications.md` | **Full copy** of `outputs/clarifications.md` |
| `outputs/repo-kit/spec/planning-sheet.csv` | **Full copy** of `outputs/planning-sheet.csv` if it exists |
| `outputs/repo-kit/spec/prd.spec.yaml` | **Full copy** of `outputs/prd.spec.yaml` if it exists |
| `outputs/repo-kit/spec/stories.spec.yaml` | **Full copy** of `outputs/stories.spec.yaml` if it exists |
| `outputs/repo-kit/spec/infographics/` | **Optional:** if `outputs/infographics/` contains assets referenced by the PRD, copy those files here so the new repo keeps self-contained design references. |
| `outputs/repo-kit/spec/digest.md` | **Prefer** full copy of `outputs/spec-digest.md`. If that file is missing, synthesize from `templates/repo-kit/spec/digest.template.md` + `outputs/prd.md` (remove HTML comments). |
| `outputs/repo-kit/spec/CHANGELOG.md` | **Prefer** full copy of `outputs/spec-changelog.md`. If missing, use `templates/repo-kit/spec/CHANGELOG.template.md` with `{{GENERATED_DATE}}`. |

## Placeholders

Replace globally in README, AGENTS, and CLAUDE.md:

- `{{PROJECT_NAME}}` — PRD title: first `#` heading in `outputs/prd.md` (strip `#` and trim), or the `<project-name>` placeholder from the template if missing.
- `{{GENERATED_DATE}}` — ISO date `YYYY-MM-DD`.

## Quality bar

- **`spec/digest.md`** must be **skimmable in under two minutes** and must list **FR/NFR**
  groupings or a compact index (not the full PRD).
- Do **not** leave `<!-- ... -->` comments in the final `digest.md` or `CHANGELOG.md`.
- Ensure **UTF-8** text; preserve markdown tables from the PRD in `spec/prd.md` verbatim on copy.
- If **`spec/architecture.md`** is copied, strip any remaining `<!-- ... -->` comments there too.
- If you copy **`outputs/infographics/`** into **`spec/infographics/`**, update **image paths inside `spec/prd.md`** so they resolve (for example `spec/infographics/INF-01-system-context.png`).

## User-facing note

After this step, tell the user:

> Copy **everything inside** `outputs/repo-kit/` to your **new repository root**, then commit. The product PRD and backlog live in `spec/`; use **`AGENTS.md`** for shared rules, plus **`CLAUDE.md`** and **`.claude/skills/`** (Claude Code), **`.github/copilot-instructions.md`** (GitHub Copilot), and **`.cursor/`** (Cursor) for tool-specific defaults.

## Next step

Continue to **`spec-sync-trackers`** if the full workflow is running and export was confirmed.
