---
name: spec-architecture-stack
description: After PRD approval, produce a high-level solution architecture and compare multiple technology-stack options so stakeholders can choose before task decomposition.
---

# Architecture and technology stack

## Purpose

Translate an approved PRD into a **high-level architecture** (containers, major
integrations, data flows, deployment shape) and a **technology stack decision
package**: several credible **stack options** with an explicit **comparison** and a
**recommended default**, so the human can pick (or edit) before **`spec-task-breakdown`**
locks engineering assumptions into epics and tasks.

## When to run

- **Automatically** in **`spec-full-workflow`** immediately after **checkpoint C**
  (PRD approved or refined) and **before** **`spec-task-breakdown`**.
- May be run standalone when the user asks for architecture / stack options only.

## Inputs

- **`outputs/prd.md`** (required) — scope, FR/NFR, constraints, non-goals.
- **`outputs/clarifications.md`** (required if present) — assumptions and open questions.
- **`outputs/prd.spec.yaml`** (optional) — structured FR/NFR ids and metadata.

## Instructions

You are a **staff engineer / architect** preparing a decision-ready memo, not a
low-level design spec.

1. **Ground in the PRD** — Respect in-scope / out-of-scope, NFRs (latency, compliance,
   tenancy, integrations), and explicit constraints. Do not invent vendor contracts
   or SLAs.
2. **High-level architecture** — Produce a concise solution outline:
   - **Context** — primary users, external systems, trust boundaries.
   - **Logical view** — major subsystems or services and responsibilities.
   - **Data** — main data stores, movement, and consistency expectations (eventual vs strong where it matters).
   - **Deployment / ops** — hosting class (SaaS, cloud region, on-prem edge) only at the level justified by the PRD.
   - Optional **Mermaid** `C4Context` or `flowchart` in the doc when it clarifies; keep diagrams small.
3. **Stack options (minimum 3, maximum 5)** — Each option must be a **coherent stack**
   (runtime, framework, primary datastore, auth/integration style, observability) that
   could plausibly deliver the PRD. Name options clearly (e.g. **Option A — …**).
4. **Comparison table** — Single markdown table comparing options on dimensions driven
   by the PRD, for example: time-to-market, operational complexity, cost posture
   (qualitative), team skill fit (if stated), security/compliance fit, vendor lock-in,
   scalability, integration effort, NFR coverage. Use **✓ / ~ / ✗** or **Low/Med/High**
   consistently; add a one-line legend.
5. **Recommendation** — State which option you recommend **for this PRD** and why
   (3–6 bullets tied to FR/NFR ids where possible).
6. **Selection placeholder** — Leave a prominent **`## Selected stack (pending)`** section
   with a short checklist the user will complete at the workflow checkpoint (or instruct
   the orchestrator to fill after the user chooses an option letter/name).
7. **Traceability** — Reference **FR-** / **NFR-** ids where architecture choices address them.

## Delegation (optional)

Steps 1–7 and the output write below are entirely **checkpoint-free** — human
**checkpoint D** only happens afterward, in the orchestrator. In a tool that supports
spawning an isolated subagent (e.g. Claude Code's `Agent` tool), the orchestrator may
run this **whole skill** in one subagent call instead of inline:

- The subagent reads **`outputs/prd.md`**, **`outputs/clarifications.md`**, and
  **`outputs/prd.spec.yaml`** (if present) itself, then writes **`outputs/architecture.md`**
  directly per this skill's own **Output format** section.
- It returns to the orchestrator only a short summary — recommended option, one-line
  comparison headline, confirmation the file was written — **not** the full file content
  or its research trail.
- The orchestrator then reads **`outputs/architecture.md`** itself (a small, finished
  file) when building **checkpoint D**, instead of carrying the research/exploration
  that produced it in its own context.

If the tool has no subagent capability, run this skill inline exactly as written above —
no behavior change.

## Output format

Write **`outputs/architecture.md`** following **`templates/architecture.md`**.

Required sections (in order):

1. Title (`# Architecture — <product>`).
2. `## Summary` — 5–10 bullets: architecture headline + stack choice ask.
3. `## High-level architecture` — subsections as needed (see template).
4. `## Technology stack options` — one subsection per option with components listed.
5. `## Comparison` — comparison table + legend.
6. `## Recommendation` — recommended option + caveats.
7. `## Selected stack (pending)` — table or bullets: chosen option name, key components,
   and “locked for decomposition” one-liner (content filled after human checkpoint).
8. `## Assumptions`
9. `## Open Questions`

Tone: decisive but honest; flag where the PRD is silent and you inferred.

## Quality bar

- Remove `<!-- ... -->` placeholder comments from the final **`outputs/architecture.md`**
  (the template may contain authoring hints).

## Human checkpoint (full workflow)

After writing `outputs/architecture.md`, the orchestrator pauses (**checkpoint D**).
The user chooses an option (or hybrid). The orchestrator then **updates**
`outputs/architecture.md`: replace **`## Selected stack (pending)`** with
**`## Selected stack (locked)`** documenting the choice and prune or mark superseded
alternatives only if needed—keep the comparison table for history unless the user
asks to remove it.

## Next step

After **checkpoint D** is cleared and **`outputs/architecture.md`** reflects the
selected stack, run **`spec-task-breakdown`** (which must align tasks with that
architecture).
