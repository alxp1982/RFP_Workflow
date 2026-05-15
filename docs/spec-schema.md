# Machine-readable spec schema (v1)

These YAML files are **canonical, agent-optimized** companions to `outputs/prd.md`
and `outputs/stories.md`. They must stay **traceability-aligned**: every `FR-*` /
`NFR-*` / `S*` id in YAML must match ids used in markdown.

| Artifact | Path | Produced by |
|----------|------|-------------|
| PRD spec | `outputs/prd.spec.yaml` | `rfp-draft-prd`, updated by `rfp-refine-prd` |
| Stories spec | `outputs/stories.spec.yaml` | `rfp-user-stories` |
| Spec digest | `outputs/spec-digest.md` | `rfp-draft-prd`, updated by `rfp-refine-prd` / `rfp-user-stories` |
| Spec changelog | `outputs/spec-changelog.md` | `rfp-draft-prd` (seed), append-only thereafter |

Skeleton templates: `templates/prd.spec.yaml`, `templates/stories.spec.yaml`.  
Worked examples for tests: `examples/minimal-prd.spec.yaml`, `examples/minimal-stories.spec.yaml`.

## Versioning

- **`spec_version`**: integer schema version (currently `1`). Bump when breaking shape changes.
- **`meta.updated_at`**: ISO date `YYYY-MM-DD` when the file was last aligned to markdown.

## ID conventions (enforced in evals)

| Kind | Pattern (regex) | Example |
|------|-----------------|--------|
| Functional requirement | `^FR-\d{2}$` | `FR-01` |
| Non-functional requirement | `^NFR-\d{2}$` | `NFR-01` |
| Story | `^S\d{2}\.\d{2}\.\d{2}$` | `S01.01.01` |
| Epic (optional in stories spec) | `^E\d{2}$` | `E01` |

*Note:* If your pipeline uses different zero-padding, widen the regex in evals and
this doc together.

---

## `prd.spec.yaml` (v1)

### Top level

| Field | Type | Required |
|-------|------|----------|
| `spec_version` | int | yes |
| `meta` | object | yes |
| `scope` | object | yes |
| `requirements` | object | yes |
| `assumptions` | list of string | yes |
| `open_questions` | list of string | yes |

### `meta`

| Field | Type | Required |
|-------|------|----------|
| `product_name` | string | yes |
| `prd_status` | string | yes — e.g. `draft`, `revised`, `final` |
| `updated_at` | string (ISO date) | yes |
| `source` | string | optional — e.g. `rfp-workflow` |

### `scope`

| Field | Type | Required |
|-------|------|----------|
| `in_scope` | list of string | yes (may be empty) |
| `out_of_scope` | list of string | yes (may be empty) |

### `requirements`

| Field | Type | Required |
|-------|------|----------|
| `functional` | list of **FR item** | yes |
| `nonfunctional` | list of **NFR item** | yes |

**FR item**

| Field | Type | Required |
|-------|------|----------|
| `id` | string (`FR-\d{2}`) | yes |
| `title` | string | yes |
| `priority` | string | optional |
| `acceptance` | list of string | optional |

**NFR item**

| Field | Type | Required |
|-------|------|----------|
| `id` | string (`NFR-\d{2}`) | yes |
| `title` | string | yes |
| `metric` | string | optional |

---

## `stories.spec.yaml` (v1)

### Top level

| Field | Type | Required |
|-------|------|----------|
| `spec_version` | int | yes |
| `meta` | object | yes |
| `stories` | list of **story item** | yes |

### `meta`

| Field | Type | Required |
|-------|------|----------|
| `product_name` | string | yes |
| `updated_at` | string (ISO date) | yes |
| `source` | string | optional |

### Story item

| Field | Type | Required |
|-------|------|----------|
| `id` | string (`S\d{2}\.\d{2}\.\d{2}`) | yes |
| `title` | string | yes |
| `epic_id` | string (`E\d{2}`) | yes |
| `persona` | string | yes |
| `user_story` | string | yes |
| `prd_trace` | list of string (`FR-\d{2}` or `NFR-\d{2}`) | yes |
| `complexity` | string | optional — `S`, `M`, `L`, `XL` |
| `scenarios` | list of **scenario item** | yes |
| `acceptance_criteria` | list of string | yes |

**Scenario item**

| Field | Type | Required |
|-------|------|----------|
| `name` | string | yes |
| `kind` | `happy` or `edge` | yes |
| `given` | list of string | yes |
| `when` | list of string | yes |
| `then` | list of string | yes |

---

## Markdown companions

### `outputs/spec-digest.md`

Short (target **under ~2 minutes** read), fixed sections:

1. One-line outcome  
2. In scope / out of scope (bullets)  
3. Requirement ID index (group FR/NFR ranges or themes)  
4. Top NFRs that affect architecture  
5. Epic → story map (compact)  
6. Open questions + assumptions (terse)

Regenerate when `prd.md` changes materially; **do not** duplicate full PRD prose.

### `outputs/spec-changelog.md`

- Append **newest first** under a `## Log` heading.
- Each block: `### YYYY-MM-DD — title` then bullets; reference ids (`FR-…`, `S…`).
- **Seed** on first PRD draft; **append** on refine and after `stories.spec.yaml` baseline.

---

## Repo kit (`outputs/repo-kit/`)

`rfp-bootstrap-repo` copies **`templates/repo-kit/`** into **`outputs/repo-kit/`** so you can paste that tree into a **new product repository’s root** (`spec/`, `AGENTS.md`, product-only Cursor/Claude rules and skills, Copilot instructions, optional `docs/` for the product codebase, and so on).

**These kit files are not RFP Workflow skills.** They do not live under this repository’s
`skills/` pipeline; they exist only as **templates** until materialized into `outputs/repo-kit/`
and copied out. Full layout: **`templates/repo-kit/README.md`**.
