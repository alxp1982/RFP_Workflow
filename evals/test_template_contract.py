"""Deterministic checks: templates and skills match workflow rules (no LLM calls)."""

from __future__ import annotations

from pathlib import Path

import pytest

REQUIRED_TEMPLATE_SNIPPETS = {
    "templates/prd.md": ("## Assumptions", "### Open Questions"),
    "templates/stories.md": ("## Assumptions", "## Open Questions"),
    "templates/clarifications.md": ("## Working Assumptions", "## Open Questions"),
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
