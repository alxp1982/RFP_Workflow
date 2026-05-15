# {{PROJECT_NAME}} — Claude Code

This product repository is **spec-driven**. Authoritative cross-tool guidance is in **`AGENTS.md`**.

## Session start

1. Read **`spec/digest.md`** first (or after a long gap).
2. Use **`spec/prd.spec.yaml`** / **`spec/stories.spec.yaml`** for compact IDs and scenarios when present.

## Implementation kickoff

For work tied to **Story IDs**, follow the skill at **`.claude/skills/project-spec-context/SKILL.md`** (same workflow as the Cursor copy under `.cursor/skills/project-spec-context/`).

## Changing requirements

Use **`.claude/skills/spec-add-requirement/SKILL.md`** to add or change FR/NFR, stories,
or backlog rows while keeping **`spec/prd.spec.yaml`** and **`spec/stories.spec.yaml`**
aligned with markdown. Then refresh **`spec/digest.md`** and **`spec/CHANGELOG.md`**
(see **`docs/living-documentation.md`**).

## Guardrails and coding baseline

Read **`docs/engineering-guidelines.md`** (stack/architecture guardrails and baseline
coding practices). Cursor loads an extra rule file: **`.cursor/rules/engineering-guardrails.mdc`**.

---

_Baseline generated: {{GENERATED_DATE}}_
