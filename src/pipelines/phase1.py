from __future__ import annotations

import pandas as pd
from datetime import datetime, UTC
from core.config import load_settings
from ingestion.crossref import fetch_source_records
from ingestion.cleaning import build_clean_dataframe
from retrieval.index import LocalEmbeddingIndex
from evaluation.testset import build_test_set
from evaluation.metrics import evaluate_pipeline
from observability.quality import run_data_quality_checks, build_freshness_report
from observability.reporting import generate_phase1_report
from core.utils import read_json, write_json

def main() -> None:
    settings = load_settings()
    
    # 2. Fetch records
    if not settings.paths.raw_records_json.exists():
        print("Fetching Crossref records...")
        records = fetch_source_records(settings)
        # It already writes to raw_records_json inside the function
    else:
        print("Loading raw records from cache...")
        from ingestion.crossref import load_raw_records
        records = load_raw_records(settings.paths.raw_records_json)
        
    print("Cleaning data...")
    df = build_clean_dataframe(records, datetime.now(UTC))
    
    print("Building Chroma index...")
    index = LocalEmbeddingIndex.build(df, settings)
    
    if not settings.paths.eval_testset.exists():
        print("Building test set...")
        build_test_set(df, settings.paths.eval_testset)
        
    print("Evaluating baseline pipeline...")
    metrics = evaluate_pipeline(
        settings, index, settings.paths.eval_testset, 
        settings.paths.baseline_metrics, settings.paths.baseline_answers
    )
    
    print("Running quality checks...")
    quality = run_data_quality_checks(df, settings, "phase1")
    freshness = build_freshness_report(df, settings, settings.paths.freshness_report)
    
    source_summary = {"extracted": len(records), "cleaned": len(df)}
    generate_phase1_report(settings.paths.baseline_report, source_summary, metrics.summary, quality, freshness)
    print(f"Phase 1 pipeline completed successfully. Report generated at {settings.paths.baseline_report}")

if __name__ == "__main__":
    main()
