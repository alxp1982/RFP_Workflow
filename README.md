# RFP Workflow Skills

A no-code, zero-setup collection of **AI assistant skills** for analyzing RFPs
and generating delivery artifacts. Works directly inside **GitHub Copilot**,
**Cursor**, and **Claude Code** -- no CLI, no service, no dependencies.

## Install with GitHub CLI skills

This repository is compatible with `gh skill install` via the standard
`skills/*/SKILL.md` layout.

References:
- GitHub CLI `gh skill` docs: `https://cli.github.com/manual/gh_skill`
- GitHub CLI `gh skill install` docs: `https://cli.github.com/manual/gh_skill_install`
- Agent Skills specification (SKILL.md format): `https://agentskills.io/specification`

Install the orchestrator skill:

```bash
gh skill install alxp1982/RFP_Workflow rfp-agentic-orchestrator
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

## Recommended mode: single agentic run

Use one orchestrator skill to execute the full chain with human-in-the-loop
checkpoints:

```text
Use #file:skills/rfp-agentic-orchestrator/SKILL.md

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
| Refined PRD (after answering questions) | `outputs/prd.md` (overwrite) |
| Technical task decomposition | `outputs/task-breakdown.md` |
| Gherkin stories with acceptance criteria | `outputs/stories.md` |
| Export to Google Sheets / GitHub / Jira | via export skill |

## Skills pipeline

```
RFP input (file or text)
       |
       v
rfp-ingest      -> normalize requirements
       |
       v
rfp-clarify     -> assumptions + open questions (non-blocking)
       |
       v
rfp-prd-draft   -> full PRD markdown
       |
       v
rfp-prd-refine  -> refined PRD after answering questions  (optional)
       |
       v
rfp-decompose   -> Epic -> Feature -> Story -> Task hierarchy
       |
       v
rfp-stories     -> Gherkin-style stories + acceptance criteria
       |
       v
rfp-export      -> Google Sheets / GitHub Projects / Jira
```

## How to use from your AI tool

### GitHub Copilot (VS Code)

Reference a skill file in Copilot Chat and provide your input:

```
Use #file:skills/rfp-prd-draft/SKILL.md

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
Run #file:skills/rfp-prd-draft/SKILL.md on: [paste RFP text or reference a file]
```

### Generic (any AI chat)

Copy a `skills/*/SKILL.md` file and paste it into the conversation, then
append your requirements text.

## Repository layout

```
skills/
  rfp-workflow/SKILL.md                Umbrella entrypoint for workflow runs
  rfp-agentic-orchestrator/SKILL.md    One-shot end-to-end orchestrator (HITL)
  rfp-ingest/SKILL.md                  Normalize raw RFP input
  rfp-clarify/SKILL.md                 Mandatory non-blocking clarification pass
  rfp-prd-draft/SKILL.md               Generate PRD
  rfp-prd-refine/SKILL.md              Refine PRD with answered questions
  rfp-decompose/SKILL.md               Decompose into task hierarchy
  rfp-stories/SKILL.md                 Generate Gherkin stories
  rfp-export/SKILL.md                  Export to external trackers

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
