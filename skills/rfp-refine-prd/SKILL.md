---
name: rfp-refine-prd
description: Refine an existing PRD draft by incorporating answers to clarification questions. Updates scope, assumptions, and open questions while preserving FR/NFR traceability IDs; keeps `prd.spec.yaml`, `spec-digest.md`, and `spec-changelog.md` aligned.
---

# Refine PRD — merge clarification answers

## Purpose
Refine the PRD draft by incorporating answers to clarification questions.

## Inputs
- PRD draft from **rfp-draft-prd** (paste or `#file:outputs/prd.md`).
- Answered clarification questions (paste answers directly).

## Instructions

You are the product manager who wrote the draft PRD. You have received answers
to some or all clarification questions.

1. Update scope, assumptions, and requirements where answers change them.
2. Remove resolved open questions; keep unresolved ones.
3. Add a `## Revision Notes` section at the top listing what changed and why.
4. Preserve FR/NFR traceability IDs -- update, do not renumber.
5. If an answer introduces new scope, flag it explicitly as `[NEW SCOPE]`.
6. **Structured companions (required):** Update **`outputs/prd.spec.yaml`** so it stays
   aligned with `outputs/prd.md` (same FR/NFR ids; refresh `meta.updated_at`).
7. Regenerate **`outputs/spec-digest.md`** from the revised PRD (same section layout as
   **`templates/spec-digest.md`**).
8. **Append** to **`outputs/spec-changelog.md`** a new **newest-first** `###` dated entry
   summarizing id-level changes (reference `FR-…`, `NFR-…`); do not delete prior entries.

## Output format

Overwrite `outputs/prd.md` with the refined PRD.

Overwrite **`outputs/prd.spec.yaml`** and **`outputs/spec-digest.md`** to match.

Append a new block at the top of the **`## Log`** section in **`outputs/spec-changelog.md`**
(newest first), per **`docs/spec-schema.md`**.

Add at the top of the PRD markdown:

```markdown
## Revision Notes
- [date]: <summary of what changed based on answers>
```

## Next step
Go to **rfp-task-breakdown**.
