# RFP Workflow Skills

A no-code, zero-setup collection of **AI assistant skills** for analyzing RFPs
and generating delivery artifacts. Use the skills **inside** GitHub Copilot,
**Cursor**, and **Claude Code** with no hosted service or extra runtime.

## Install with Skillfish

This repository is compatible with [skillfish](https://github.com/knoxgraeme/skillfish), the skill manager for AI coding agents.

Install the full pipeline skill:

```bash
skillfish add alxp1982/RFP_Workflow rfp-full-workflow
```

Install the umbrella workflow skill:

```bash
skillfish add alxp1982/RFP_Workflow rfp-workflow
```

Install all available skills from this repository:

```bash
skillfish add alxp1982/RFP_Workflow --all
```

## Install with `npx skills` (skills.sh / Vercel skills CLI)

This repository matches the [open agent skills](https://agentskills.io) layout (`skills/<name>/SKILL.md`), so it installs with the official **[skills](https://github.com/vercel-labs/skills)** CLI ([docs](https://skills.sh/docs)).

[![skills.sh](https://skills.sh/b/alxp1982/RFP_Workflow)](https://skills.sh/alxp1982/RFP_Workflow)

List skills without installing:

```bash
npx skills add alxp1982/RFP_Workflow --list
```

Install the full pipeline skill (pick agents interactively, or pin e.g. Cursor + Claude Code):

```bash
npx skills add alxp1982/RFP_Workflow --skill rfp-full-workflow -a cursor -a claude-code -y
```

Install the umbrella workflow skill:

```bash
npx skills add alxp1982/RFP_Workflow --skill rfp-workflow -a cursor -y
```

Install **every** skill from this repo (non-interactive):

```bash
npx skills add alxp1982/RFP_Workflow --skill '*' -y
```

From a local clone (same as published GitHub layout):

```bash
npx skills add . --list
npx skills add . --skill rfp-full-workflow -y
```

The CLI writes into each agent’s configured skills directory (for example **Cursor** uses the paths described under [Supported agents](https://github.com/vercel-labs/skills#supported-agents)). This repo also keeps **`skills/`** as the canonical copy and documents symlinks for other layouts in **Multi-agent scaffold compatibility** below.

## Install with GitHub CLI skills

This repository is compatible with `gh skill install` via the standard
`skills/*/SKILL.md` layout.

References:
- GitHub CLI `gh skill` docs: `https://cli.github.com/manual/gh_skill`
- GitHub CLI `gh skill install` docs: `https://cli.github.com/manual/gh_skill_install`
- Agent Skills specification (SKILL.md format): `https://agentskills.io/specification`

Install the full pipeline skill:

```bash
gh skill install alxp1982/RFP_Workflow rfp-full-workflow
```

Install the umbrella workflow skill:

```bash
gh skill install alxp1982/RFP_Workflow rfp-workflow
```

List available skills from this repository:

```bash
gh skill install alxp1982/RFP_Workflow
```

### Multi-agent scaffold compatibility

`skills/` is the canonical source of truth. For scaffold compatibility, these
directories are symlinked to `skills/`:
- `.agent/skills`
- `.claude/skills`
- `.cursor/skills`
- `.github/skills`

## Recommended mode: full pipeline (one shot)

Use the **full pipeline** skill (`rfp-full-workflow`) to execute the full chain with human-in-the-loop
checkpoints. It starts with a **Planning summary** (goals, pipeline,
checkpoints, risks) for alignment—similar to planning mode—then runs the stages.

```text
Use #file:skills/rfp-full-workflow/SKILL.md

Input: [paste RFP text or #file:path]
PRD target: local-md | google-sheets | <mcp-target>
Stories target: local-md | github | jira | <mcp-target>
```

You do **not** need to invoke each skill manually.

## What it does

Paste raw client requirements and run the skills in sequence to produce:

| Artifact | Output |
|---|---|
| Clarification questions + assumptions | `outputs/clarifications.md` |
| Product Requirements Document | `outputs/prd.md` |
| Machine-readable PRD spec | `outputs/prd.spec.yaml` |
| Spec digest & changelog (agent context) | `outputs/spec-digest.md`, `outputs/spec-changelog.md` |
| Refined PRD (after answering questions) | `outputs/prd.md` (overwrite) |
| Technical task decomposition | `outputs/task-breakdown.md` |
| Gherkin stories with acceptance criteria | `outputs/stories.md` |
| Machine-readable stories spec | `outputs/stories.spec.yaml` |
| **New product repo kit** (spec-driven baseline: `spec/`, `AGENTS.md`, `CLAUDE.md`, `.cursor/`, `.claude/`, `.github/copilot-instructions.md`) | `outputs/repo-kit/` (copy tree to a fresh repo root) |
| Export to Google Sheets / GitHub / Jira | via `rfp-sync-trackers` skill |

## Bootstrapping a new product repository

After a full pipeline run, **`outputs/repo-kit/`** contains a **ready-to-copy tree**
(`spec/` copies of the PRD and backlog, optional **`prd.spec.yaml`** / **`stories.spec.yaml`**, **`AGENTS.md`**, **`CLAUDE.md`** for Claude Code, **`.github/copilot-instructions.md`** for GitHub Copilot, **`.cursor/`** rules plus **`project-spec-context`** skill, and the same skill under **`.claude/skills/`**). Copy **the contents of `repo-kit/`** into the root
of a new empty git repository, commit, and start implementation with spec-driven
agent defaults. Templates for this kit live under **`templates/repo-kit/`**; the
**`rfp-bootstrap-repo`** skill defines exact paths and placeholder rules.

## Skills pipeline

```
RFP input (file or text)
       |
       v
rfp-normalize-rfp      -> normalize requirements
       |
       v
rfp-clarification-pass     -> assumptions + open questions (non-blocking)
       |
       v
rfp-draft-prd   -> full PRD markdown
       |
       v
rfp-refine-prd  -> refined PRD after answering questions  (optional)
       |
       v
rfp-task-breakdown   -> Epic -> Feature -> Story -> Task hierarchy
       |
       v
rfp-user-stories     -> Gherkin-style stories + acceptance criteria
       |
       v
rfp-bootstrap-repo   -> portable `outputs/repo-kit/` for a new product git repo
       |
       v
rfp-sync-trackers      -> Google Sheets / GitHub Projects / Jira
```

## How to use from your AI tool

### GitHub Copilot (VS Code)

Reference a skill file in Copilot Chat and provide your input:

```
Use #file:skills/rfp-draft-prd/SKILL.md

Requirements:
[paste RFP text here]
```

Chain skills across a session using `#file:` for each stage.
`.github/copilot-instructions.md` pre-loads the workflow context automatically.

### Cursor

`.cursor/rules/rfp-workflow.mdc` loads automatically. Then:

```
Run the PRD draft skill on the following requirements: [paste text]
```

Or open any skill file and use Cmd+L to chat against it directly.

### Claude Code

Reference the installable skill path directly:

```
Run #file:skills/rfp-draft-prd/SKILL.md on: [paste RFP text or reference a file]
```

### Generic (any AI chat)

Copy a `skills/*/SKILL.md` file and paste it into the conversation, then
append your requirements text.

## Repository layout

```
skills/
  rfp-workflow/SKILL.md                Repo entry — points at full pipeline skill
  rfp-full-workflow/SKILL.md           One-shot pipeline with human checkpoints
  rfp-normalize-rfp/SKILL.md           Turn raw RFP into structured requirements
  rfp-clarification-pass/SKILL.md      Questions + assumptions (non-blocking)
  rfp-draft-prd/SKILL.md               Write PRD from requirements
  rfp-refine-prd/SKILL.md              Update PRD after clarification answers
  rfp-task-breakdown/SKILL.md          Epic → Feature → Story → Task plan
  rfp-user-stories/SKILL.md            Gherkin-style acceptance stories
  rfp-sync-trackers/SKILL.md           Push artifacts to Sheets / GitHub / Jira

templates/
  prd.md                     Canonical PRD template
  stories.md                 Canonical stories template
  clarifications.md          Clarifications report template
  task-breakdown.md          Task hierarchy template

.github/
  copilot-instructions.md    Copilot workspace instructions

.cursor/
  rules/rfp-workflow.mdc     Cursor rules file

docs/
  architecture.md            Pipeline design notes
  integration/
    google-sheets.md         Sheets export mapping
    github-projects.md       GitHub Projects export mapping
    jira.md                  Jira export mapping

examples/
  sample-rfp.md              Sample RFP input
  sample-outputs/            Expected output artifacts
```

## Design principles

- **No code to run.** Every skill is a prompt + output template.
- **Tool-agnostic.** Works in any AI assistant.
- **Non-blocking clarifications.** Ambiguity becomes assumptions, never a
  hard stop.
- **Fixed hierarchy.** PRD -> Epic -> Feature -> Story -> AC -- every time.
- **Traceable.** Every artifact carries `assumptions` and `open_questions`.
- **Flexible output targets.** Default local markdown; export skills handle
  Sheets / GitHub / Jira.
