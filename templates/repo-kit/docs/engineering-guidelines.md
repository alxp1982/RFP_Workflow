# Engineering guidelines — architecture guardrails and coding baseline

These guidelines complement **`spec/`**. If anything here conflicts with **`spec/prd.md`**
or **`## Selected stack (locked)`** in **`spec/architecture.md`**, the spec wins until
the team explicitly changes it.

## Architecture and stack guardrails

1. **Honor the locked stack** — Use the languages, runtimes, datastores, and hosting
   choices recorded under **`## Selected stack (locked)`** in **`spec/architecture.md`**.
   Switching major components requires updating that section (and usually an ADR) first.
2. **Respect boundaries** — Do not bypass trust boundaries or integrations described in
   **`spec/architecture.md`** (e.g. calling a datastore directly from a client if the
   architecture forbids it).
3. **NFRs are requirements** — Latency, security, tenancy, and compliance called out in
   the PRD apply to every change; add tests or checks where they are at risk.
4. **Scope** — No shadow features: if it is not traced to an FR/NFR or approved Story,
   do not ship it in the same release train without updating **`spec/`** (see
   **spec-add-requirement** skill).

## Baseline coding practices

- **Small, reviewable changes** — Prefer incremental PRs over large unreviewable batches.
- **Tests follow stories** — At minimum, cover happy path + one edge per Story you touch;
   reference Story id in test description or PR text when helpful.
- **Observability** — Log/metric/trace hooks for new services or critical paths as implied
   by NFRs; avoid PII in logs unless explicitly designed and approved.
- **Secrets** — Never commit secrets; use environment or secret manager patterns aligned
   with the locked stack.
- **Dependencies** — Pin versions where the stack doc implies reproducible builds; note
   major upgrades in **`spec/CHANGELOG.md`** or **`docs/adr/`**.

## Language-specific notes

Add subsections below as the team agrees (style guide, formatter, linter commands).
Until then, match the dominant style of the existing repository.

```markdown
## TypeScript (example)

- Strict mode where applicable; no implicit any in new code.
- …

## Python (example)

- …
```

## Where to go deeper

- **`AGENTS.md`** — session defaults and tool entry points.
- **`.cursor/rules/spec-driven-product.mdc`** — spec-first discipline in Cursor.
- **`docs/living-documentation.md`** — how to keep docs in sync with development.
