"""Pick the LLM used as judge for DeepEval GEval metrics."""

from __future__ import annotations

import os
from typing import Optional

from deepeval.models.base_model import DeepEvalBaseLLM


def get_geval_judge_model() -> Optional[DeepEvalBaseLLM]:
    """
    Prefer Anthropic when ANTHROPIC_API_KEY is set; else OpenAI when OPENAI_API_KEY is set.
    Return None only when neither key is available (tests should skip before calling).
    """
    if os.getenv("ANTHROPIC_API_KEY"):
        from deepeval.models.llms.anthropic_model import AnthropicModel

        # Dateless IDs (Claude 4.x); override with ANTHROPIC_MODEL_NAME if your org differs.
        model_name = os.getenv("ANTHROPIC_MODEL_NAME", "claude-sonnet-4-6")
        return AnthropicModel(model=model_name)
    if os.getenv("OPENAI_API_KEY"):
        from deepeval.models.llms.openai_model import GPTModel

        return GPTModel()
    return None
