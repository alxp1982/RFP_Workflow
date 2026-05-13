"""
LLM-as-judge coverage for RFP → PRD-style artifacts using DeepEval (GEval).

Set **ANTHROPIC_API_KEY** (recommended for this repo) or **OPENAI_API_KEY** in the
environment or in a repo-root `.env` file (loaded by `evals/conftest.py`).

Optional: **ANTHROPIC_MODEL_NAME** (default `claude-sonnet-4-6`).

Run (show **quality metrics** + **trace-style tree**; use ``-s`` so output is not captured)::

    pytest evals/test_deepeval_prd_coverage.py -m integration -v -s

For native DeepEval trace rendering (``@observe`` spans + dashboard), use::

    deepeval test run evals/test_deepeval_prd_coverage.py -m integration

References: https://deepeval.com/
"""

from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

from evals.eval_reporting import run_llm_eval_with_reports
from evals.geval_judge import get_geval_judge_model

pytestmark = pytest.mark.integration

requires_judge = pytest.mark.skipif(
    not (os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")),
    reason="Set ANTHROPIC_API_KEY or OPENAI_API_KEY for GEval (see evals/conftest.py + .env).",
)


@requires_judge
def test_prd_covers_acme_sample_rfp_with_golden_copy(
    sample_rfp_text: str,
    golden_acme_prd: str,
) -> None:
    from deepeval.metrics import GEval
    from deepeval.test_case import LLMTestCase
    from deepeval.test_case.llm_test_case import SingleTurnParams

    judge = get_geval_judge_model()
    assert judge is not None

    t_load = time.perf_counter()
    rfp_in = sample_rfp_text
    prd_out = golden_acme_prd
    load_ms = (time.perf_counter() - t_load) * 1000

    coverage = GEval(
        name="RFP_to_PRD_requirement_coverage",
        criteria=(
            "Given the INPUT (raw RFP), does the ACTUAL_OUTPUT (PRD) "
            "substantively address the stated requirements (auth, directory, HR, news, "
            "documents/RBAC, mobile, performance, EU/GDPR, Workday, admin) without inventing "
            "contradictory facts? Score higher when each major RFP theme appears with "
            "clear intent to implement or specify it."
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        threshold=0.7,
        async_mode=False,
        model=judge,
    )

    test_case = LLMTestCase(input=rfp_in, actual_output=prd_out)
    ok = run_llm_eval_with_reports(
        test_node_id="test_prd_covers_acme_sample_rfp_with_golden_copy",
        test_case=test_case,
        metrics=[coverage],
        retriever_label="load_rfp_and_prd",
        retriever_detail="sample-rfp.md + golden_acme_employee_portal_prd.md",
        retriever_duration_ms=load_ms,
    )
    assert ok, "GEval threshold not met; see Metrics Summary and trace above."


@requires_judge
def test_user_prd_path_optional_regression(
    sample_rfp_text: str,
    repo_root: Path,
) -> None:
    """Point RFP_EVAL_PRD_PATH at a generated prd.md that matches the same RFP as examples/sample-rfp.md."""
    from deepeval.metrics import GEval
    from deepeval.test_case import LLMTestCase
    from deepeval.test_case.llm_test_case import SingleTurnParams

    path_str = os.getenv("RFP_EVAL_PRD_PATH")
    if not path_str:
        pytest.skip("Set RFP_EVAL_PRD_PATH to a PRD markdown file to run this regression.")

    prd_path = Path(path_str).expanduser()
    if not prd_path.is_absolute():
        prd_path = (repo_root / prd_path).resolve()
    if not prd_path.is_file():
        pytest.fail(f"RFP_EVAL_PRD_PATH is not a file: {prd_path}")

    judge = get_geval_judge_model()
    assert judge is not None

    t_load = time.perf_counter()
    actual = prd_path.read_text(encoding="utf-8")
    load_ms = (time.perf_counter() - t_load) * 1000

    metric = GEval(
        name="RFP_to_PRD_alignment",
        criteria=(
            "Given INPUT as the RFP and ACTUAL_OUTPUT as the PRD, evaluate whether the PRD "
            "reflects the RFP's scope and constraints. Penalize major omissions or fabricated "
            "requirements not supported by the RFP."
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        threshold=0.65,
        async_mode=False,
        model=judge,
    )
    ok = run_llm_eval_with_reports(
        test_node_id="test_user_prd_path_optional_regression",
        test_case=LLMTestCase(input=sample_rfp_text, actual_output=actual),
        metrics=[metric],
        retriever_label="load_prd_from_path",
        retriever_detail=str(prd_path),
        retriever_duration_ms=load_ms,
    )
    assert ok, "GEval threshold not met; see Metrics Summary and trace above."
