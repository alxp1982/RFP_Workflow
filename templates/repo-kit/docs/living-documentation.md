# Living documentation

Keep documentation **as current as the code** so agents and humans share the same mental model.

## What counts as documentation

| Area | Location | When to update |
|------|----------|----------------|
| Product truth | `spec/prd.md`, `spec/stories.md`, YAML specs | Any scope or acceptance change (use **`.cursor/skills/spec-add-requirement/SKILL.md`** or the Claude copy under **`.claude/skills/`**). |
| Agent skim | `spec/digest.md` | After meaningful PRD/story/breakdown edits. |
| History | `spec/CHANGELOG.md` | Every spec batch (append, newest first). |
| Architecture / stack | `spec/architecture.md` | When boundaries, integrations, or **locked** stack components change. |
| Runtime / ops | `docs/` (this tree), README, runbooks | New envs, deploy steps, on-call playbooks, data migrations. |
| Decisions | `docs/adr/` (create if needed) | Irreversible or costly choices; link from CHANGELOG when relevant. |

## Habits (low overhead)

1. **Same PR as the code** — Prefer doc updates in the PR that introduces the behavior; avoid “doc later” unless tracked as a follow-up Story.
2. **Link to ids** — Reference **FR-/NFR-** and **Story IDs** in ADRs and runbooks so traceability stays grep-friendly.
3. **Digest is not a dump** — Keep `spec/digest.md` under ~2 minutes’ read; move depth to `spec/prd.md` or `docs/`.
4. **Changelog entries are cheap** — One short block per merge that touched `spec/` is enough: date, title, bullet list of ids.

## Anti-patterns

- Updating only markdown **or** only YAML — always pair when both exist.
- Stale diagrams — Regenerate or delete diagrams that no longer match deployment or data flow.
- Hidden assumptions — If you inferred behavior, put it in **Assumptions** or an ADR, not only in chat.
