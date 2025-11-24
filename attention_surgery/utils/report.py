"""
Markdown report generation for Attention Surgery runs.
"""
from datetime import datetime
from typing import Dict, List, Sequence

from ..core.cache import AblationConfig, HeadId, RunResult


def _format_heads(heads: Sequence[HeadId]) -> str:
    if not heads:
        return "None"
    return ", ".join([f"({layer},{head})" for layer, head in heads])


def _format_metrics(metrics: Dict[str, float]) -> str:
    if not metrics:
        return "No metrics available."
    lines = []
    for key, value in metrics.items():
        lines.append(f"- **{key}**: {value:.4f}")
    return "\n".join(lines)


def generate_surgery_report(
    run_result: RunResult,
    ablation_config: AblationConfig,
    top_k_heads: List[HeadId],
    shareable: bool = True,
) -> str:
    """
    Compose a markdown report summarizing a single surgery run.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    header = "# Attention Surgery Report"
    meta_block = (
        f"- **Time**: {timestamp}\n"
        f"- **Prompt**: {run_result.prompt}\n"
        f"- **Ablation Method**: `{ablation_config.method}`\n"
        f"- **Target Heads**: {_format_heads(ablation_config.heads)}\n"
        f"- **Top-K Critical Heads**: {_format_heads(top_k_heads)}"
    )

    metrics_block = "## Metrics Overview\n" + _format_metrics(run_result.metrics)

    text_block = (
        "## Generated Text Comparison\n"
        "### Original Output\n"
        f"{run_result.generated_text_original}\n\n"
        "### Ablated Output\n"
        f"{run_result.generated_text_ablated}"
    )

    importance_lines = []
    if run_result.importance_scores:
        importance_lines.append("## Importance Scores\n")
        for method, scores in run_result.importance_scores.items():
            sorted_scores = sorted(
                scores.items(), key=lambda kv: kv[1], reverse=True
            )[:10]
            formatted = ", ".join(
                [f"({layer},{head}): {value:.4f}" for (layer, head), value in sorted_scores]
            )
            importance_lines.append(f"- **{method}**: {formatted or 'None'}")
    else:
        importance_lines.append("## Importance Scores\nNo data available.")

    share_hint = (
        "\n> You can share this report directly with collaborators." if shareable else ""
    )

    return "\n\n".join(
        [header, meta_block, metrics_block, text_block, *importance_lines]
    ) + share_hint

