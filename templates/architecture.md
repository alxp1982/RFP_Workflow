# Architecture — <project name>

## Summary

- <!-- 3–6 bullets: problem framing, architectural approach, and how stack choice supports PRD goals -->
- <!-- End with one line: "Stack decision: see options below; recommendation in §Recommendation." -->

## High-level architecture

### Context

<!-- Who uses the system, external actors, major integrations (tie to FR/NFR ids). -->

### Logical view

<!-- Major components/services and responsibilities; keep vendor-neutral unless PRD names vendors. -->

### Data and consistency

<!-- Primary stores, critical flows, consistency model where NFRs demand it. -->

### Deployment and operations

<!-- Hosting model, environments, key ops concerns (only what PRD implies or NFRs require). -->

### Diagrams (optional)

```mermaid
%% Small context or container diagram if helpful
```

## Technology stack options

### Option A — <short label>

| Layer | Choice | Notes |
|-------|--------|-------|
| Runtime / language | | |
| Application framework | | |
| API style | | |
| Primary datastore | | |
| Auth / identity | | |
| Async / messaging | | |
| Hosting | | |
| Observability | | |

### Option B — <short label>

| Layer | Choice | Notes |
|-------|--------|-------|
| Runtime / language | | |
| Application framework | | |
| API style | | |
| Primary datastore | | |
| Auth / identity | | |
| Async / messaging | | |
| Hosting | | |
| Observability | | |

### Option C — <short label>

| Layer | Choice | Notes |
|-------|--------|-------|
| Runtime / language | | |
| Application framework | | |
| API style | | |
| Primary datastore | | |
| Auth / identity | | |
| Async / messaging | | |
| Hosting | | |
| Observability | | |

<!-- Add Option D / E only if they are materially different and justified by the PRD. -->

## Comparison

| Dimension | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| <!-- e.g. Time to market --> | | | |
| <!-- e.g. Operational complexity --> | | | |
| <!-- e.g. Security / compliance fit --> | | | |
| <!-- e.g. Cost posture (qualitative) --> | | | |
| <!-- e.g. Integration effort --> | | | |

_Legend: <!-- e.g. ✓ = strong fit, ~ = acceptable, ✗ = poor fit -->_

## Recommendation

**Recommended:** <!-- Option X -->

- <!-- Bullet tied to FR/NFR -->
- <!-- Tradeoff explicitly acknowledged -->

## Selected stack (pending)

| Field | Value |
|-------|-------|
| Chosen option | <!-- user or orchestrator fills after checkpoint D --> |
| Locked for decomposition at | <!-- ISO date --> |

**Locked components (summary):** <!-- one short paragraph after selection -->

## Assumptions

- <!-- PRD-silent areas you inferred -->

## Open Questions

- <!-- Questions that affect architecture or stack but are unanswered in the PRD -->
