---
name: rfp-prd-refine
description: Refine an existing PRD draft by incorporating answers to clarification questions. Updates scope, assumptions, and open questions while preserving FR/NFR traceability IDs.
---

# Skill 04 - PRD Refine

## Purpose
Refine the PRD draft by incorporating answers to clarification questions.

## Inputs
- PRD draft from **rfp-prd-draft** (paste or `#file:outputs/prd.md`).
- Answered clarification questions (paste answers directly).

## Instructions

You are the product manager who wrote the draft PRD. You have received answers
to some or all clarification questions.

1. Update scope, assumptions, and requirements where answers change them.
2. Remove resolved open questions; keep unresolved ones.
3. Add a `## Revision Notes` section at the top listing what changed and why.
4. Preserve FR/NFR traceability IDs -- update, do not renumber.
5. If an answer introduces new scope, flag it explicitly as `[NEW SCOPE]`.

## Output format

Overwrite `outputs/prd.md` with the refined PRD.
Add at the top:

```markdown
## Revision Notes
- [date]: <summary of what changed based on answers>
```

## Next step
Go to **rfp-decompose**.
