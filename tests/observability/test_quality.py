import pandas as pd
from unittest.mock import MagicMock
from observability.quality import run_data_quality_checks, build_freshness_report

def test_run_data_quality_checks(tmp_path):
    settings = MagicMock()
    settings.paths.quality_dir = tmp_path
    settings.freshness_threshold_days = 10
    
    df = pd.DataFrame([
        {"paper_id": "1", "title": "A", "summary_chars": 20, "age_days": 5},
        {"paper_id": "1", "title": "", "summary_chars": 5, "age_days": 15},
    ])
    
    result = run_data_quality_checks(df, settings, "test_report")
    assert result["row_count"] == 2
    assert result["duplicate_paper_ids"] == 1
    assert result["null_titles"] == 1
    assert result["short_summaries"] == 1
    assert result["stale_rows"] == 1
    assert result["is_healthy"] is False

def test_build_freshness_report(tmp_path):
    settings = MagicMock()
    settings.freshness_threshold_days = 10
    report_path = tmp_path / "freshness.json"
    
    df = pd.DataFrame([
        {"published_dt": "2024-01-01", "age_days": 5},
        {"published_dt": "2023-01-01", "age_days": 400},
    ])
    
    result = build_freshness_report(df, settings, report_path)
    assert result["total_rows"] == 2
    assert result["stale_rows"] == 1
    assert result["is_fresh"] is False
