"""Shared paths for RFP workflow evaluation tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]

# Load repo .env before DeepEval reads ANTHROPIC_API_KEY / OPENAI_API_KEY (does not override shell env).
load_dotenv(REPO_ROOT / ".env", override=False)
load_dotenv(REPO_ROOT / ".env.local", override=False)


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def sample_rfp_text(repo_root: Path) -> str:
    path = repo_root / "examples" / "sample-rfp.md"
    if not path.is_file():
        pytest.skip(f"Missing sample RFP: {path}")
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def golden_acme_prd(repo_root: Path) -> str:
    path = repo_root / "evals" / "test_data" / "golden_acme_employee_portal_prd.md"
    if not path.is_file():
        pytest.skip(f"Missing golden PRD: {path}")
    return path.read_text(encoding="utf-8")
