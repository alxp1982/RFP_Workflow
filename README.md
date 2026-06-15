# Spec Workflow Skills

A no-code, zero-setup collection of **AI assistant skills** for turning requirements
input into delivery artifacts. Use the skills **inside** GitHub Copilot,
**Cursor**, and **Claude Code** with no hosted service or extra runtime.

## Install with Skillfish

This repository is compatible with [skillfish](https://github.com/knoxgraeme/skillfish), the skill manager for AI coding agents.

Install the full pipeline skill:

```bash
skillfish add alxp1982/RFP_Workflow spec-full-workflow
```

Install the umbrella workflow skill:

```bash
skillfish add alxp1982/RFP_Workflow spec-workflow
```

Install the update workflow skill:

```bash
skillfish add alxp1982/RFP_Workflow spec-update
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
npx skills add alxp1982/RFP_Workflow --skill spec-full-workflow -a cursor -a claude-code -y
```

Install the umbrella workflow skill:

```bash
npx skills add alxp1982/RFP_Workflow --skill spec-workflow -a cursor -y
```

Install **every** skill from this repo (non-interactive):

```bash
npx skills add alxp1982/RFP_Workflow --skill '*' -y
```

From a local clone (same as published GitHub layout):

```bash
npx skills add . --list
npx skills add . --skill spec-full-workflow -y
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
gh skill install alxp1982/RFP_Workflow spec-full-workflow
```

Install the umbrella workflow skill:

```bash
gh skill install alxp1982/RFP_Workflow spec-workflow
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

## Notion meeting notes (optional input)

Pull **meeting notes** from Notion into the pipeline using the official
[Notion MCP](https://developers.notion.com/guides/mcp/overview) server. Works for
**initial runs** (`spec-full-workflow`) and **updates** (`spec-update`).

You can pass either:

- **Notion page URL(s)** — fetch known pages directly
- **Search string** — search your workspace; if several pages match, pick from a table
- **Both** — always include listed URLs plus any extra pages from search

Fetched content is written to **`outputs/notion-input.md`**, then normalized like
any other requirements input.

### Install Notion MCP

Full reference: [`docs/integration/notion.md`](docs/integration/notion.md)

#### Cursor (recommended)

1. Open **Cursor Settings → MCP → Add new global MCP server**
2. Paste:

```json
{
  "mcpServers": {
    "notion": {
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

3. Save and **restart Cursor**
4. On first use of a Notion tool, complete the **OAuth** flow in the browser

**Team / project config:** copy [`.cursor/mcp.json.example`](.cursor/mcp.json.example)
to `.cursor/mcp.json` in this repo (each teammate still authorizes OAuth locally).

#### VS Code / GitHub Copilot

Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

Command Palette → **MCP: List Servers** → start Notion → complete OAuth.

#### Claude Code

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

Run `/mcp` in Claude Code and authenticate.

#### Other MCP clients (stdio-only)

If your client does not support remote HTTP MCP servers:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.notion.com/mcp"]
    }
  }
}
```

### Run with Notion input

**Initial pipeline:**

```text
Use #file:skills/spec-full-workflow/SKILL.md

Notion search: "Q2 product discovery notes"
```

```text
Use #file:skills/spec-full-workflow/SKILL.md

Notion URLs:
- https://www.notion.so/myworkspace/Sprint-Planning-abc123def4567890abcdef1234567890
```

**Update pipeline:**

```text
Use #file:skills/spec-update/SKILL.md

Notion search: "architecture review follow-up"
Scope: auto
```

Install the Notion fetch skill explicitly (optional):

```bash
skillfish add alxp1982/RFP_Workflow spec-notion-input
```

## Recommended mode: full pipeline (one shot)

Use the **full pipeline** skill (`spec-full-workflow`) to execute the full chain with human-in-the-loop
checkpoints. It starts with a **Planning summary** (goals, pipeline,
checkpoints, risks) for alignment—similar to planning mode—then runs the stages.

```text
Use #file:skills/spec-full-workflow/SKILL.md

Input: [paste requirements text or #file:path]
# or Notion meeting notes:
Notion search: "discovery workshop"
Notion URLs:
- https://www.notion.so/...

PRD target: local-md | google-sheets | <mcp-target>
Stories target: local-md | github | jira | <mcp-target>
```

You do **not** need to invoke each skill manually.

## Update mode: merge new information later

When `outputs/` already has artifacts from a prior run and you receive **new
information** (clarification answers, review comments, scope changes), use
**`spec-update`** instead of re-running the full pipeline:

```text
Use #file:skills/spec-update/SKILL.md

New information: [paste answers, feedback, or scope changes]
# or Notion:
Notion search: "sprint retro action items"

Scope: auto | prd-only | prd+breakdown | full
```

The update workflow assesses impact (T1 PRD → T4 full downstream), merges deltas,
keeps FR/NFR/Story ids stable, and appends to **`outputs/spec-changelog.md`**.

## What it does

Paste raw client requirements and run the skills in sequence to produce:

| Artifact | Output |
|---|---|
| Clarification questions + assumptions | `outputs/clarifications.md` |
| Product Requirements Document | `outputs/prd.md` |
| Machine-readable PRD spec | `outputs/prd.spec.yaml` |
| Spec digest & changelog (agent context) | `outputs/spec-digest.md`, `outputs/spec-changelog.md` |
| Refined PRD (after answering questions) | `outputs/prd.md` (overwrite) |
| Architecture & technology stack options | `outputs/architecture.md` |
| Technical task decomposition | `outputs/task-breakdown.md` |
| Gherkin stories with acceptance criteria | `outputs/stories.md` |
| Machine-readable stories spec | `outputs/stories.spec.yaml` |
| **New product repo kit** (spec-driven baseline: `spec/`, `AGENTS.md`, `CLAUDE.md`, `.cursor/`, `.claude/`, `.github/copilot-instructions.md`) | `outputs/repo-kit/` (copy tree to a fresh repo root) |
| Export to Google Sheets / GitHub / Jira | via `spec-sync-trackers` skill |

## Bootstrapping a new product repository

After a full pipeline run, **`outputs/repo-kit/`** contains a **ready-to-copy tree**
for a **new product git repository** (see **`templates/repo-kit/README.md`** for the full layout: `spec/`, `AGENTS.md`, product-only Cursor/Claude rules and **nested** skills, Copilot instructions, optional `docs/` guides, and so on). **Those nested skills and `docs/` are not part of this Spec Workflow repo’s `skills/` pipeline**—they ship only inside the kit for use **after** you copy `repo-kit/` into the product repo root. Copy **the contents of `repo-kit/`** into the root
of a new empty git repository, commit, and start implementation with spec-driven
agent defaults. The **`spec-bootstrap-repo`** skill defines exact paths and placeholder rules.

## Skills pipeline

```
Requirements input (file, text, or Notion via MCP)
       |
       v
[spec-notion-input]     -> outputs/notion-input.md (optional)
       |
       v
spec-normalize-input      -> normalize requirements
       |
       v
spec-clarification-pass     -> assumptions + open questions (non-blocking)
       |
       v
spec-draft-prd   -> full PRD markdown
       |
       v
spec-refine-prd  -> refined PRD after answering questions  (optional)
       |
       v
spec-architecture-stack -> architecture memo + stack comparison + selection
       |
       v
spec-task-breakdown   -> Epic -> Feature -> Story -> Task hierarchy
       |
       v
spec-user-stories     -> Gherkin-style stories + acceptance criteria
       |
       v
spec-bootstrap-repo   -> portable `outputs/repo-kit/` for a new product git repo
       |
       v
spec-sync-trackers      -> Google Sheets / GitHub Projects / Jira
```

**Update path** (when artifacts already exist):

```
New information + existing outputs/
       |
       v
spec-update             -> impact assessment + delta merge
       |
       +--> spec-refine-prd (+ downstream stages per impact tier)
```

## How to use from your AI tool

### GitHub Copilot (VS Code)

Reference a skill file in Copilot Chat and provide your input:

```
Use #file:skills/spec-draft-prd/SKILL.md

Requirements:
[paste requirements text here]
```

Chain skills across a session using `#file:` for each stage.
`.github/copilot-instructions.md` pre-loads the workflow context automatically.

### Cursor

`.cursor/rules/spec-workflow.mdc` loads automatically. Then:

```
Run the PRD draft skill on the following requirements: [paste text]
```

Or open any skill file and use Cmd+L to chat against it directly.

### Claude Code

Reference the installable skill path directly:

```
Run #file:skills/spec-draft-prd/SKILL.md on: [paste requirements text or reference a file]
```

### Generic (any AI chat)

Copy a `skills/*/SKILL.md` file and paste it into the conversation, then
append your requirements text.

## Repository layout

```
skills/
  spec-workflow/SKILL.md                Repo entry — full pipeline or update workflow
  spec-full-workflow/SKILL.md           One-shot pipeline with human checkpoints
  spec-update/SKILL.md                  Merge new info into existing artifacts
  spec-notion-input/SKILL.md            Fetch meeting notes from Notion (MCP)
  spec-normalize-input/SKILL.md         Turn raw input into structured requirements
  spec-clarification-pass/SKILL.md      Questions + assumptions (non-blocking)
  spec-draft-prd/SKILL.md               Write PRD from requirements
  spec-refine-prd/SKILL.md              Update PRD after clarification answers
  spec-architecture-stack/SKILL.md      Architecture + stack options before breakdown
  spec-task-breakdown/SKILL.md          Epic → Feature → Story → Task plan
  spec-user-stories/SKILL.md            Gherkin-style acceptance stories
  spec-bootstrap-repo/SKILL.md          Materialize `outputs/repo-kit/` for a new repo
  spec-sync-trackers/SKILL.md           Push artifacts to Sheets / GitHub / Jira

templates/
  prd.md                     Canonical PRD template
  stories.md                 Canonical stories template
  clarifications.md          Clarifications report template
  task-breakdown.md          Task hierarchy template

.github/
  copilot-instructions.md    Copilot workspace instructions

.cursor/
  rules/spec-workflow.mdc     Cursor rules file

docs/
  architecture.md            Pipeline design notes
  integration/
    notion.md                  Notion MCP input (meeting notes)
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
- **Fixed hierarchy.** PRD → architecture & stack → Epic → Feature → Story → Task — every time.
- **Traceable.** Every artifact carries `assumptions` and `open_questions`.
- **Notion input.** Optional **`spec-notion-input`** fetches meeting notes via MCP (URLs or search) for initial runs and updates.
- **Incremental updates.** `spec-update` merges late-arriving information without restarting from scratch.
- **Export review gates.** Checkpoint **G** shows epic/story summary tables; **G2** reviews each story before Jira/GitHub create.
- **Flexible output targets.** Default local markdown; export skills handle
  Sheets / GitHub / Jira.
