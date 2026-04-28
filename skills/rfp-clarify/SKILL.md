---
name: rfp-clarify
description: Run a mandatory, non-blocking clarification pass on normalized RFP requirements. Produces clarification questions, working assumptions, and open questions without halting the workflow.
---

# Skill 02 - Clarify

## Purpose
Run a mandatory, non-blocking clarification pass on normalized requirements.
Always produces a clarification report even if input is unambiguous.
Never halts the workflow -- all findings become assumptions or open questions.

## Inputs
- Normalized requirements from **rfp-ingest** (paste or `#file:`).

## Instructions

You are an expert product manager reviewing requirements before writing a PRD.

For EVERY input, produce a clarification report with:
1. **Clarification questions** - specific questions that, if answered, would
   meaningfully improve scope precision. Keep them concise and numbered.
2. **Working assumptions** - reasonable defaults you will apply if questions
   go unanswered. Be explicit so stakeholders can correct them.
3. **Open questions** - items you cannot assume away and that need an answer
   before implementation starts (mark these separately).

Rules:
- Non-blocking: always continue even if questions are unresolved.
- At minimum produce 2 working assumptions even on clear requirements.
- Deduplicate; max 10 clarification questions.
- Severity: mark each question as `[low]`, `[medium]`, or `[high]`.

## Output format

Save as `outputs/clarifications.md`:

```markdown
## Clarifications: <project-name>

### Clarification Questions
- [high] Q1: ...
- [medium] Q2: ...

### Working Assumptions
- A1: ...
- A2: ...

### Open Questions (need answer before implementation)
- OQ1: ...
```

## Next step
Pass this output (along with normalized requirements) to **rfp-prd-draft**.
If clarification answers are collected, skip to **rfp-prd-refine** instead.
