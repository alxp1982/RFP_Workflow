# Notion input (meeting notes)

## Purpose

Use **Notion MCP** to pull meeting notes (or other pages) into the spec pipeline
as `outputs/notion-input.md`, then:

- **Initial run:** `spec-notion-input` → `spec-normalize-input` → … → `spec-full-workflow`
- **Update run:** `spec-notion-input` (mode `update`) → `spec-update`

## Install Notion MCP

Official docs: [Connecting to Notion MCP](https://developers.notion.com/guides/mcp/get-started-with-mcp)

### Cursor (global)

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

3. Save and restart Cursor.
4. On first Notion tool use, complete the **OAuth** flow.

### Cursor / team (project-level)

Create `.cursor/mcp.json` in the repo root with the same JSON block so teammates
share the connector config (each user still completes OAuth locally).

### VS Code / GitHub Copilot

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

Run **MCP: List Servers** from the Command Palette, start Notion, and complete OAuth.

### Claude Code

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

Then run `/mcp` and authenticate.

### Clients without remote HTTP support

Use the `mcp-remote` bridge:

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

## Input modes

| You provide | Skill behavior |
|-------------|----------------|
| **Notion page URL(s)** | Fetch those pages directly |
| **Search string** | Search workspace; if multiple hits, user picks pages from a table |
| **Both** | Fetch URLs first, then search and merge (dedupe by page id) |

Skill: `skills/spec-notion-input/SKILL.md`

## Output artifact

| File | Contents |
|------|----------|
| `outputs/notion-input.md` | Metadata + markdown body per fetched page |

In **update** mode, new captures are **prepended** (newest first); prior captures are kept.

## Orchestrator entry points

**Full workflow** — include Notion params in the same message as `spec-full-workflow`:

```text
Use #file:skills/spec-full-workflow/SKILL.md

Notion search: "Q2 discovery notes"
# or
Notion URLs:
- https://www.notion.so/...
```

**Update workflow:**

```text
Use #file:skills/spec-update/SKILL.md

Notion search: "post-review action items"
Scope: auto
```

## Permissions

- Notion MCP uses **your** OAuth identity; the agent only sees pages you can open.
- Enterprise workspaces may restrict MCP clients in Notion **Settings → Connections → Notion MCP**.

## See also

- `skills/spec-notion-input/SKILL.md`
- README.md § Notion meeting notes
