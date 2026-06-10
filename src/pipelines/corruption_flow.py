from __future__ import annotations

from datetime import datetime, UTC
from core.config import load_settings
from core.utils import read_json
from ingestion.cleaning import build_clean_dataframe
from ingestion.corruption import build_unprocessed_dataframe
from ingestion.crossref import load_raw_records
from retrieval.index import LocalEmbeddingIndex
from evaluation.metrics import evaluate_pipeline
from observability.quality import run_data_quality_checks, build_freshness_report
from observability.reporting import generate_corruption_report

def main() -> None:
    settings = load_settings()
    
    print("Loading baseline records...")
    records = load_raw_records(settings.paths.raw_records_json)
    clean_df = build_clean_dataframe(records, datetime.now(UTC))
    baseline_metrics = read_json(settings.paths.baseline_metrics)
    
    print("Corrupting data (Using Raw Unprocessed Data)...")
    corrupt_df = build_unprocessed_dataframe(records, settings.paths.corruption_log)
    
    print("Evaluating corrupted data...")
    corrupted_index = LocalEmbeddingIndex.build(corrupt_df, settings, settings.paths.corrupted_embeddings_json)
    corrupted_eval = evaluate_pipeline(
        settings, corrupted_index, settings.paths.eval_testset,
        settings.paths.corrupted_metrics, settings.paths.corrupted_answers
    )
    corrupted_quality = run_data_quality_checks(corrupt_df, settings, "corrupted")
    corrupted_freshness = build_freshness_report(corrupt_df, settings, settings.paths.quality_dir / "corrupted_freshness.json")
    
    print("Repairing data...")
    repaired_df = build_clean_dataframe(records, datetime.now(UTC))
    repaired_index = LocalEmbeddingIndex.build(repaired_df, settings, settings.paths.repaired_embeddings_json)
    repaired_eval = evaluate_pipeline(
        settings, repaired_index, settings.paths.eval_testset,
        settings.paths.repaired_metrics, settings.paths.repaired_answers
    )
    repaired_quality = run_data_quality_checks(repaired_df, settings, "repaired")
    repaired_freshness = build_freshness_report(repaired_df, settings, settings.paths.quality_dir / "repaired_freshness.json")
    
    generate_corruption_report(
        settings.paths.comparison_report,
        baseline_metrics,
        corrupted_eval.summary,
        repaired_eval.summary,
        corrupted_quality,
        repaired_quality,
        corrupted_freshness,
        repaired_freshness,
    )
    print(f"Corruption flow completed. Report generated at {settings.paths.comparison_report}")

if __name__ == "__main__":
    main()
