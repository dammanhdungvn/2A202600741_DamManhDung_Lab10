from __future__ import annotations

from typing import Any
import pandas as pd
from core.config import Settings
from core.utils import write_json

def run_data_quality_checks(df: pd.DataFrame, settings: Settings, report_name: str) -> dict[str, Any]:
    row_count = len(df)
    
    null_paper_ids = df['paper_id'].isnull().sum() if 'paper_id' in df.columns else 0
    duplicate_paper_ids = df['paper_id'].duplicated().sum() if 'paper_id' in df.columns else 0
    
    null_titles = df['title'].replace("", pd.NA).isnull().sum() if 'title' in df.columns else 0
    
    short_summaries = (df['summary_chars'] < 10).sum() if 'summary_chars' in df.columns else 0
    
    stale_rows = (df['age_days'] > settings.freshness_threshold_days).sum() if 'age_days' in df.columns else 0
    
    quality_metrics = {
        "report_name": report_name,
        "row_count": int(row_count),
        "null_paper_ids": int(null_paper_ids),
        "duplicate_paper_ids": int(duplicate_paper_ids),
        "null_titles": int(null_titles),
        "short_summaries": int(short_summaries),
        "stale_rows": int(stale_rows),
        "is_healthy": bool(
            null_paper_ids == 0 and 
            duplicate_paper_ids == 0 and 
            null_titles == 0 and 
            short_summaries == 0
        )
    }
    
    report_path = settings.paths.quality_dir / f"{report_name}_quality.json"
    write_json(report_path, quality_metrics)
    
    return quality_metrics


def build_freshness_report(df: pd.DataFrame, settings: Settings, report_path) -> dict[str, Any]:
    if len(df) == 0:
        return {}
        
    latest_published = df['published_dt'].max() if 'published_dt' in df.columns else None
    oldest_published = df['published_dt'].min() if 'published_dt' in df.columns else None
    
    stale_rows = int((df['age_days'] > settings.freshness_threshold_days).sum()) if 'age_days' in df.columns else 0
    total_rows = len(df)
    
    is_fresh = (stale_rows / total_rows) < 0.2 if total_rows > 0 else False
    
    payload = {
        "latest_published": str(latest_published),
        "oldest_published": str(oldest_published),
        "stale_rows": stale_rows,
        "total_rows": total_rows,
        "is_fresh": is_fresh
    }
    
    write_json(report_path, payload)
    return payload
