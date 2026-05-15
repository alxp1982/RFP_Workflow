# {{PROJECT_NAME}} — generated repo kit

This folder was produced by the **RFP Workflow** `rfp-bootstrap-repo` step. It is
meant to be copied **as the root of a new product repository** (or merged into
an empty repo) so coding agents inherit **spec-driven** context: backlog, PRD,
stories, and **Cursor / Claude Code / GitHub Copilot** hooks aligned to this product.

## How to use

1. Create a new empty git repository (for example on GitHub, then `git clone`).
2. Copy **everything inside this `repo-kit/` directory** into that repo root:
   - You should see `.cursor/`, `.claude/`, `.github/`, `spec/`, `AGENTS.md`,
     `CLAUDE.md`, and this `README.md` at the root of the new repo — not nested under
     `outputs/` or `repo-kit/`.
3. Commit: `git add -A && git commit -m "chore: bootstrap product spec and agent context"`.
4. Open the repo in **Cursor**, **Claude Code**, or **VS Code with Copilot**. Defaults:
   **`AGENTS.md`**, **`.github/copilot-instructions.md`**, **`CLAUDE.md`**, and
   **`.cursor/rules/spec-driven-product.mdc`** (Cursor-only).

## Layout

| Path | Purpose |
|------|--------|
| `AGENTS.md` | Cross-tool agent instructions (spec-first, IDs, hierarchy). |
| `CLAUDE.md` | Claude Code root pointer → `AGENTS.md` + `spec/digest.md`. |
| `.github/copilot-instructions.md` | GitHub Copilot repo instructions (spec-driven defaults). |
| `.cursor/rules/spec-driven-product.mdc` | Cursor rule: prefer `spec/` for product truth. |
| `.cursor/skills/project-spec-context/` | Cursor skill: digest + targeted spec slices. |
| `.claude/skills/project-spec-context/` | Claude Code skill (same intent as Cursor skill). |
| `spec/digest.md` | Short **default context** for agents (regenerate when PRD changes). |
| `spec/CHANGELOG.md` | Baseline and **append-only** spec deltas for long sessions. |
| `spec/prd.md` | Full PRD (human-readable). |
| `spec/stories.md` | Gherkin stories + tracker metadata. |
| `spec/task-breakdown.md` | Epic → Feature → Story → Task plan. |
| `spec/clarifications.md` | Clarification pass output. |
| `spec/planning-sheet.csv` | Planning / sizing sheet. |

## Hierarchy (fixed)

`Epic → Feature → Story → Task` — do not rename levels; trace work to **FR/NFR**
and **Story IDs** from `spec/`.

## Optional next steps

- Add application code under `src/` (or your stack’s convention).
- Replace `.gitignore` if you need language-specific ignores beyond the baseline.
- When the PRD changes materially, update `spec/digest.md` and append to
  `spec/CHANGELOG.md` (or re-run the bootstrap skill from the RFP workflow repo).

_Generated: {{GENERATED_DATE}}_
