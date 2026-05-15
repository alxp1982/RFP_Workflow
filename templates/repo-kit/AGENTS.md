# Agent instructions — {{PROJECT_NAME}}

This repository was bootstrapped from an RFP workflow run. **Product and backlog
truth** live under `spec/`. Prefer those files over chat memory.

## Default context (low token)

1. Read **`spec/digest.md`** first every session (or when returning after a long gap).
2. For dense / low-token context, prefer **`spec/prd.spec.yaml`** and **`spec/stories.spec.yaml`**
   (lists, ids, structured scenarios) when they exist; use markdown for long-form review.
3. Load **only** the slices you need next:
   - **`spec/stories.md`** — for acceptance / Gherkin and Story IDs.
   - **`spec/prd.md`** — for FR/NFR detail, NFRs, and scope.
   - **`spec/task-breakdown.md`** — for dependencies and the Epic → Feature → Story → Task tree.
4. Append **`spec/CHANGELOG.md`** (last ~20 lines) if the user references recent spec changes.

## Rules

- **Traceability:** Implementation and tests must map to **FR-/NFR-** IDs and **Story IDs**
  (from `spec/stories.md` / `spec/task-breakdown.md`). Say which IDs you are satisfying in PR descriptions when helpful.
- **Hierarchy:** Do not flatten Epic/Feature/Story/Task; preserve naming from the breakdown.
- **Assumptions & open questions:** Respect `## Assumptions` and `## Open Questions` in
  `spec/prd.md` and `spec/stories.md`. Surface conflicts instead of silently overriding.
- **Non-goals:** Honor explicit out-of-scope items in the PRD.

## Tool-specific entry points

- **Cursor:** `@.cursor/skills/project-spec-context/SKILL.md` when starting implementation
  on a set of stories (pass Story IDs in chat). Rule: `.cursor/rules/spec-driven-product.mdc`.
- **Claude Code:** project skill `.claude/skills/project-spec-context/SKILL.md` (same
  workflow). Root **`CLAUDE.md`** points here and to **`AGENTS.md`**.
- **GitHub Copilot:** `.github/copilot-instructions.md` is loaded as repo context; it defers
  to **`AGENTS.md`** and **`spec/`** for full rules.

## When to read full `spec/prd.md`

Use the full PRD for legal/compliance-heavy sections, architecture sign-off, or when
`spec/digest.md` explicitly points to a section. Otherwise avoid pasting the entire PRD
into every turn.

---

_Baseline generated: {{GENERATED_DATE}}_
