---
name: rfp-prd-draft
description: Generate a complete Product Requirements Document from normalized requirements and a clarification report. Includes proposed-solution infographics (via GenerateImage or Mermaid) and preserves FR/NFR traceability.
---

# Skill 03 - PRD Draft

## Purpose
Generate a full Product Requirements Document from normalized requirements and
the clarification report.

## Inputs
- Normalized requirements from **rfp-ingest**.
- Clarification report from **rfp-clarify**.
- Optional: PRD template file (`#file:templates/prd.md`).
- Image-generation skill `nano-banana` (use it when available in the environment).

## Instructions

You are a senior product manager writing a PRD for an engineering team.

Using the requirements and clarifications provided:
1. Write a complete PRD following the output template exactly.
2. Embed all working assumptions in the Assumptions section.
3. List all open questions in the Open Questions section.
4. Keep scope crisp -- do not expand beyond stated requirements.
5. Each requirement in the Scope section must be traceable to an FR/NFR from
   the ingest output (use the FR-/NFR- IDs).
6. Write in plain, imperative language.
7. You MUST generate proposed-solution infographics and reference them in the PRD using whatever tools are available (e.g. GenerateImage tool, Mermaid diagrams, etc.).

## Infographic generation rules

- Generate visual assets only for the **proposed solution**, not decorative art.
- Prefer 1-3 visuals maximum:
   1. system/context diagram
   2. end-to-end user flow
   3. phased launch / MVP scope visual
- Use clean product/consulting style visuals suitable for inclusion in a PRD.
- Base visuals only on stated requirements plus explicit assumptions.
- Avoid brand-infringing logos, copyrighted UI copies, or invented vendor claims.
- Save references in the PRD under `High Level Approach -> Proposed Solution`
  and `UX / Content / Accessibility -> Design References`.

### Required invocation

Create these assets in `outputs/infographics/` with exact file names:
- `INF-01-system-context` (png or svg)
- `INF-02-user-flow` (png or svg)
- `INF-03-mvp-phasing` (png or svg)

Use image generation tools or text-based diagrams (like Mermaid) to create modern, professional architecture diagrams:

1) **System/context diagram**
A modern, professional tech infographic showing the system context. E.g.: Customers (web/mobile) -> Modern Portal -> Identity/MFA, Order+Shipment services, Reporting service, and Support platform. Style: clean consulting diagram, balanced mix of simple icons and structured blocks, blue/gray palette, easy to read for a PRD.

2) **End-to-end user flow**
A modern user journey flowchart for portal MVP. E.g.: Sign in + MFA -> Dashboard -> Order History -> Shipment Tracking -> Report Export. Style: clean, structured flowchart with simple, professional iconography to represent steps, clear directional arrows.

3) **MVP phasing visual**
A modern, professional project phasing diagram with 3 phases: Foundation, MVP Delivery, Hardening/Go-live. Include key deliverables per phase. Style: clean consulting roadmap, visually appealing but highly organized, using distinct columns or timeline steps.

After generation:
- **CRITICAL:** If your image generation tool saves the images to a global/external `assets/` folder (like Cursor's GenerateImage tool does), you MUST use shell commands to move those images into `outputs/infographics/` in this repository workspace.
- Update the PRD to reference the new RELATIVE paths (e.g. `outputs/infographics/INF-01-system-context.png`) under `Proposed Solution Infographics` and `Design References`. Do not use absolute paths.

If no image generation tools or diagramming tools are available at all:
- Do not block PRD generation.
- Insert placeholders describing the recommended visuals to create later.

## Output format

Save as `outputs/prd.md`. Use the template at `templates/prd.md`.
Key sections that must be present:
- Problem Alignment
- High Level Approach
- Solution Alignment
- Launch Plan
- Functional requirements (traced to FR-IDs)
- Non-functional requirements (traced to NFR-IDs)
- Proposed solution infographics (generated or placeholder references)
- Assumptions
- Open questions
- FAQs
- Changelog

## Next step
- If clarification answers are available: go to **rfp-prd-refine**.
- Otherwise: go to **rfp-decompose**.
