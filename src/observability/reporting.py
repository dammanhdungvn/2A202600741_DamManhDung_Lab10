from __future__ import annotations
from typing import Any
from core.utils import write_text

def generate_phase1_report(
    report_path,
    source_summary: dict[str, Any],
    metrics: dict[str, Any],
    quality: dict[str, Any],
    freshness: dict[str, Any],
) -> None:
    content = f"""# Phase 1 Baseline Report

## Source Summary
- Extracted: {source_summary.get('extracted', 0)}
- Cleaned: {source_summary.get('cleaned', 0)}

## Data Quality
- Is Healthy: {quality.get('is_healthy', False)}
- Null Titles: {quality.get('null_titles', 0)}
- Freshness: {freshness.get('is_fresh', False)} (Stale rows: {freshness.get('stale_rows', 0)})

## Evaluation Metrics
- Hit Rate: {metrics.get('retrieval_hit_rate', 0):.2%}
- Token F1: {metrics.get('mean_token_f1', 0):.2%}
- LLM Judge Accuracy: {metrics.get('judge_accuracy', 0):.2%}
"""
    write_text(report_path, content)

def generate_corruption_report(
    report_path,
    baseline_metrics: dict[str, Any],
    corrupted_metrics: dict[str, Any],
    repaired_metrics: dict[str, Any],
    corrupted_quality: dict[str, Any],
    repaired_quality: dict[str, Any],
    corrupted_freshness: dict[str, Any],
    repaired_freshness: dict[str, Any],
) -> None:
    content = f"""# Corruption vs Repair Report

## Quality comparison
- Corrupted Is Healthy: {corrupted_quality.get('is_healthy', False)}
- Repaired Is Healthy: {repaired_quality.get('is_healthy', False)}

## Metrics Comparison
- Baseline Hit Rate: {baseline_metrics.get('retrieval_hit_rate', 0):.2%}
- Corrupted Hit Rate: {corrupted_metrics.get('retrieval_hit_rate', 0):.2%}
- Repaired Hit Rate: {repaired_metrics.get('retrieval_hit_rate', 0):.2%}
"""
    write_text(report_path, content)
