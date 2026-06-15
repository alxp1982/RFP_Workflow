---
name: spec-normalize-input
description: Parse raw requirements input (pasted text or a file like requirements.pdf / requirements.md) into a structured, normalized requirements summary covering functional requirements, non-functional requirements, stakeholders, and constraints. Use as the first step of the spec workflow.
---

# Normalize input — structured requirements

## Purpose
Parse and normalize raw requirements input (document or text) into a structured
requirements summary ready for downstream skills.

## Inputs
Provide ONE of:
- The full text of the requirements pasted directly into the chat.
- A file reference (e.g. `#file:requirements.pdf` or `#file:examples/sample-rfp.md`).

## Instructions

You are an expert business analyst. Given the raw requirements input below, produce a
normalized requirements summary following the output format exactly.

Rules:
1. Extract only stated requirements. Do not invent scope.
2. Separate functional requirements (what the system must do) from
   non-functional requirements (performance, security, compliance, UX).
3. Identify named stakeholders and their roles if mentioned.
4. Note any stated constraints (timeline, budget, tech stack).
5. Flag anything ambiguous as a candidate for clarification.
6. Use plain language; avoid marketing phrases.

## Output format

```markdown
## Normalized Requirements: <project-name>

### Functional Requirements
- FR-01: ...
- FR-02: ...

### Non-Functional Requirements
- NFR-01: ...
- NFR-02: ...

### Stakeholders
- <Role>: <description>

### Constraints
- <constraint>

### Ambiguities (candidates for clarification)
- <item>
```

## Next step
Pass the output of this skill to **spec-clarification-pass**.
