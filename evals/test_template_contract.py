"""Deterministic checks: templates and skills match workflow rules (no LLM calls)."""

from __future__ import annotations

from pathlib import Path

import pytest

REQUIRED_TEMPLATE_SNIPPETS = {
    "templates/prd.md": ("## Assumptions", "### Open Questions"),
    "templates/stories.md": ("## Assumptions", "## Open Questions"),
    "templates/clarifications.md": ("## Working Assumptions", "## Open Questions"),
    "templates/architecture.md": ("## Assumptions", "## Open Questions"),
    "templates/spec-digest.md": ("## One-line outcome", "## Requirement ID index"),
    "templates/spec-changelog.md": ("## Log",),
}


@pytest.mark.parametrize("rel_path,needles", list(REQUIRED_TEMPLATE_SNIPPETS.items()))
def test_templates_include_assumptions_and_open_questions(
    repo_root: Path, rel_path: str, needles: tuple[str, ...]
) -> None:
    text = (repo_root / rel_path).read_text(encoding="utf-8")
    for needle in needles:
        assert needle in text, f"{rel_path} must contain {needle!r}"


def test_golden_acme_prd_exists_and_matches_template_sections(repo_root: Path) -> None:
    golden = repo_root / "evals" / "test_data" / "golden_acme_employee_portal_prd.md"
    assert golden.is_file(), f"Missing golden PRD: {golden}"
    text = golden.read_text(encoding="utf-8")
    assert "## Assumptions" in text
    assert "### Open Questions" in text
    assert "FR-01" in text and "NFR-01" in text


def test_repo_kit_templates_exist_and_have_placeholders(repo_root: Path) -> None:
    readme = repo_root / "templates" / "repo-kit" / "README.md"
    assert readme.is_file()
    assert "{{PROJECT_NAME}}" in readme.read_text(encoding="utf-8")
    digest_tpl = repo_root / "templates" / "repo-kit" / "spec" / "digest.template.md"
    assert digest_tpl.is_file()
    assert "{{PROJECT_NAME}}" in digest_tpl.read_text(encoding="utf-8")
    changelog_tpl = repo_root / "templates" / "repo-kit" / "spec" / "CHANGELOG.template.md"
    assert changelog_tpl.is_file()
    assert "{{GENERATED_DATE}}" in changelog_tpl.read_text(encoding="utf-8")
    rule = repo_root / "templates" / "repo-kit" / ".cursor" / "rules" / "spec-driven-product.mdc"
    assert rule.is_file()
    ctx_skill = (
        repo_root
        / "templates"
        / "repo-kit"
        / ".cursor"
        / "skills"
        / "project-spec-context"
        / "SKILL.md"
    )
    raw = ctx_skill.read_text(encoding="utf-8")
    assert raw.startswith("---\n")
    assert "name: project-spec-context" in raw.split("---", 2)[1]

    claude_ctx = (
        repo_root
        / "templates"
        / "repo-kit"
        / ".claude"
        / "skills"
        / "project-spec-context"
        / "SKILL.md"
    )
    assert claude_ctx.is_file()
    claude_raw = claude_ctx.read_text(encoding="utf-8")
    assert claude_raw == raw, "Claude and Cursor project-spec-context skills should match"

    copilot = repo_root / "templates" / "repo-kit" / ".github" / "copilot-instructions.md"
    assert copilot.is_file()
    copilot_text = copilot.read_text(encoding="utf-8")
    assert "AGENTS.md" in copilot_text and "spec/digest.md" in copilot_text

    claude_md = repo_root / "templates" / "repo-kit" / "CLAUDE.md"
    assert claude_md.is_file()
    claude_tpl = claude_md.read_text(encoding="utf-8")
    assert "{{PROJECT_NAME}}" in claude_tpl and "{{GENERATED_DATE}}" in claude_tpl

    add_req = (
        repo_root
        / "templates"
        / "repo-kit"
        / ".cursor"
        / "skills"
        / "spec-add-requirement"
        / "SKILL.md"
    )
    assert add_req.is_file()
    add_raw = add_req.read_text(encoding="utf-8")
    assert add_raw.startswith("---\n")
    assert "name: spec-add-requirement" in add_raw.split("---", 2)[1]

    claude_add = (
        repo_root
        / "templates"
        / "repo-kit"
        / ".claude"
        / "skills"
        / "spec-add-requirement"
        / "SKILL.md"
    )
    assert claude_add.is_file()
    assert claude_add.read_text(encoding="utf-8") == add_raw

    living = repo_root / "templates" / "repo-kit" / "docs" / "living-documentation.md"
    assert living.is_file() and "Living documentation" in living.read_text(encoding="utf-8")

    eng = repo_root / "templates" / "repo-kit" / "docs" / "engineering-guidelines.md"
    assert eng.is_file() and "Selected stack (locked)" in eng.read_text(encoding="utf-8")

    guard = repo_root / "templates" / "repo-kit" / ".cursor" / "rules" / "engineering-guardrails.mdc"
    assert guard.is_file()
    assert "engineering-guidelines.md" in guard.read_text(encoding="utf-8")


def test_spec_schema_doc_exists(repo_root: Path) -> None:
    path = repo_root / "docs" / "spec-schema.md"
    text = path.read_text(encoding="utf-8")
    assert "prd.spec.yaml" in text and "stories.spec.yaml" in text


def test_skill_files_have_yaml_frontmatter(repo_root: Path) -> None:
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        pytest.skip("No skills/ directory at repo root")
    skill_files = list(skills_dir.rglob("SKILL.md"))
    assert skill_files, "expected at least one skills/**/SKILL.md"
    for path in skill_files:
        raw = path.read_text(encoding="utf-8")
        assert raw.startswith("---\n"), f"{path.relative_to(repo_root)} must start with YAML frontmatter"
        assert "name:" in raw.split("---", 2)[1], f"{path.relative_to(repo_root)} frontmatter must set name:"
