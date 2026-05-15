# Spec-driven product repository

This repository was bootstrapped for **spec-first** development. Treat **`spec/`** as the source of truth for product requirements, backlog, and acceptance criteria.

## Before you change code

1. Read **`spec/digest.md`** for a short picture of scope and requirement IDs.
2. Prefer **`spec/prd.spec.yaml`** and **`spec/stories.spec.yaml`** for id lists and structured scenarios when they exist; use **`spec/prd.md`** and **`spec/stories.md`** for narrative detail.
3. If **`spec/architecture.md`** exists, align implementation with **`## Selected stack (locked)`** and the high-level architecture; do not swap stacks silently.
4. Follow **`AGENTS.md`** for traceability, hierarchy, and session defaults (it applies across Cursor, Claude Code, and Copilot).
5. For **new or changed requirements**, follow the same workflow as **`spec-add-requirement`** in `.cursor/skills/` / `.claude/skills/`: keep **`spec/prd.md`** / **`spec/prd.spec.yaml`** and **`spec/stories.md`** / **`spec/stories.spec.yaml`** in sync, then update **`spec/digest.md`** and **`spec/CHANGELOG.md`** (see **`docs/living-documentation.md`**).
6. Respect **`docs/engineering-guidelines.md`** (locked stack, boundaries, baseline coding). Cursor users also get **`.cursor/rules/engineering-guardrails.mdc`**.

## Rules

- **Traceability:** Map implementation and tests to **FR-** / **NFR-** IDs and **Story IDs** from `spec/stories.md` and `spec/task-breakdown.md`.
- **Hierarchy:** Preserve **Epic → Feature → Story → Task** naming from `spec/task-breakdown.md`; do not flatten or rename levels.
- **Scope:** Do not invent requirements beyond **`spec/prd.md`** / **`spec/prd.spec.yaml`** without an explicit change request. Respect **Assumptions** and **Open Questions** in the spec.

## When the PRD or stories change

Update **`spec/digest.md`** and append **`spec/CHANGELOG.md`** so agents stay aligned.
