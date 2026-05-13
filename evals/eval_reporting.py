"""Console reporting for DeepEval runs: quality metrics + trace-style tree (Rich)."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, Sequence

from rich.console import Console
from rich.text import Text
from rich.tree import Tree

if TYPE_CHECKING:
    from deepeval.evaluate.types import TestResult
    from deepeval.metrics import BaseMetric
    from deepeval.test_case import LLMTestCase


@dataclass
class _SpanSpec:
    span_type: str  # AGENT, RETRIEVER, LLM, TOOL
    name: str
    duration_ms: float
    metric_line: Optional[str] = None


def _clip(s: str, max_len: int = 72) -> str:
    s = s.replace("\n", " ").strip()
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."


def _type_style(span_type: str) -> str:
    return {
        "AGENT": "bold magenta",
        "RETRIEVER": "bold cyan",
        "LLM": "bold green",
        "TOOL": "bold yellow",
    }.get(span_type, "bold white")


def _span_label(sp: _SpanSpec) -> Text:
    line = Text()
    line.append(f"{sp.span_type}: ", style=_type_style(sp.span_type))
    line.append(sp.name, style="default")
    if sp.metric_line:
        line.append("  ")
        line.append(sp.metric_line, style="dim")
    line.append(f"  ({sp.duration_ms:.0f}ms)", style="dim")
    return line


def print_compact_metrics_summary(test_result: "TestResult") -> None:
    """Print scores and clipped judge reasons (avoids dumping full PRD to the console)."""
    from deepeval.evaluate.types import TestResult

    if not isinstance(test_result, TestResult) or not test_result.metrics_data:
        return

    print("\n" + "=" * 70 + "\n")
    print("Metrics Summary\n")
    for md in test_result.metrics_data:
        ok = bool(md.success) and md.error is None
        mark = "✅" if ok else "❌"
        reason = md.reason or ""
        if len(reason) > 400:
            reason = reason[:397] + "..."
        err = f", error: {md.error}" if md.error else ""
        print(
            f"  {mark} {md.name} (score: {md.score}, threshold: {md.threshold}){err}\n"
            f"      reason: {reason}\n"
        )
    print("")


def print_eval_trace_tree(
    *,
    test_name: str,
    agent_name: str,
    agent_duration_ms: float,
    children: Sequence[_SpanSpec],
    trace_score: Optional[float],
    metrics_passed: int,
    metrics_total: int,
    overall_passed: bool,
) -> None:
    """Print a hierarchical trace similar to ``deepeval test run`` terminal output."""
    console = Console()
    root = Tree(Text(test_name, style="bold"))

    agent_branch = root.add(_span_label(_SpanSpec("AGENT", agent_name, agent_duration_ms)))
    for sp in children:
        agent_branch.add(_span_label(sp))

    console.print(root)
    parts: List[str] = []
    if trace_score is not None:
        parts.append(f"Trace score: {trace_score:.2f}")
    parts.append(f"Metric count: {metrics_passed}/{metrics_total} metrics passed")
    console.print("  " + " | ".join(parts))

    status = "PASSED" if overall_passed else "FAILED"
    style = "bold white on green" if overall_passed else "bold white on red"
    console.print(Text(f" {status} ", style=style))


def run_llm_eval_with_reports(
    *,
    test_node_id: str,
    test_case: "LLMTestCase",
    metrics: List["BaseMetric"],
    retriever_label: str,
    retriever_detail: str,
    retriever_duration_ms: float,
) -> bool:
    """
    Run DeepEval metrics with console output:

    - **Trace-style tree** (Rich): AGENT → RETRIEVER + LLM nodes with timings and scores.
    - **Metrics Summary**: per-metric score, threshold, and clipped judge ``reason``.
    - **Overall pass rates** block (DeepEval helper) for the single test case.

    Returns whether all metrics passed (same criterion as ``assert_test``).

    Use ``pytest -s`` (or ``--capture=no``) so Rich output and plain-text summaries are visible.
    """
    from deepeval.evaluate import evaluate
    from deepeval.evaluate.configs import AsyncConfig, DisplayConfig
    from deepeval.evaluate.utils import aggregate_metric_pass_rates

    t_total = time.perf_counter()

    children: List[_SpanSpec] = [
        _SpanSpec(
            span_type="RETRIEVER",
            name=f"{retriever_label}({_clip(retriever_detail)})",
            duration_ms=retriever_duration_ms,
            metric_line="deterministic",
        ),
    ]

    t_llm = time.perf_counter()
    result = evaluate(
        [test_case],
        metrics=metrics,
        async_config=AsyncConfig(run_async=False),
        display_config=DisplayConfig(
            show_indicator=False,
            print_results=False,
            verbose_mode=None,
        ),
    )
    llm_ms = (time.perf_counter() - t_llm) * 1000

    tr = result.test_results[0]
    if not tr.metrics_data:
        raise RuntimeError("DeepEval returned no metrics_data")

    scores: List[float] = []
    passed_n = 0
    n_metrics = len(tr.metrics_data)
    per_llm_ms = llm_ms / max(n_metrics, 1)

    for md in tr.metrics_data:
        ok = bool(md.success) and md.error is None
        if ok:
            passed_n += 1
        if md.score is not None:
            scores.append(float(md.score))
        if md.error:
            mline = f"error  ✗  {md.error}"
        else:
            sym = "✓" if ok else "✗"
            sc = f"{float(md.score):.2f}" if md.score is not None else "n/a"
            mline = f"score: {sc} (threshold {md.threshold})  {sym}"
        children.append(
            _SpanSpec(
                span_type="LLM",
                name=md.name,
                duration_ms=per_llm_ms,
                metric_line=mline,
            )
        )

    agent_ms = (time.perf_counter() - t_total) * 1000
    trace_score = sum(scores) / len(scores) if scores else None

    print_eval_trace_tree(
        test_name=test_node_id,
        agent_name="rfp_workflow_llm_eval",
        agent_duration_ms=agent_ms,
        children=children,
        trace_score=trace_score,
        metrics_passed=passed_n,
        metrics_total=n_metrics,
        overall_passed=bool(tr.success),
    )
    print_compact_metrics_summary(tr)
    aggregate_metric_pass_rates([tr])

    return bool(tr.success)