---
name: project-spec-context
description: Load product spec and backlog from this repo's spec/ tree for spec-driven implementation. Use at kickoff of a coding task or when switching Story IDs.
---

# Project spec context

## Purpose

Attach the **right** product context for implementation: default low-token load,
then drill into PRD/stories by ID.

## Instructions

1. Read **`spec/digest.md`** end-to-end.
2. If **`spec/prd.spec.yaml`** / **`spec/stories.spec.yaml`** exist, use them for the
   **id index**, **prd_trace**, and **scenario lists** for the requested work before
   pulling large markdown blocks.
3. If **`spec/architecture.md`** exists, skim **`## Selected stack (locked)`** (or pending)
   before pulling infra-specific detail from the PRD alone.
4. If the user named **Story IDs** (for example `S01.02.03`), open only the matching
   blocks in **`spec/stories.md`** and the related rows/sections in
   **`spec/task-breakdown.md`**.
5. For functional detail, pull **only** the **FR-/NFR-** sections from **`spec/prd.md`**
   (or the corresponding objects in **`spec/prd.spec.yaml`**) that those stories trace to.
6. If the user mentions recent changes, read the tail of **`spec/CHANGELOG.md`**.
7. Respect **`AGENTS.md`** and do not expand scope beyond the spec without explicit approval.

## Outputs (agent behavior)

- Propose plans and code **tagged** to Story and FR/NFR IDs where applicable.
- Call out conflicts with **Assumptions** or **Open Questions** in the spec instead of guessing.

## Inputs (from user)

Optional: comma-separated **Story IDs**, or “epic E01”, or “FR-12 only”.
