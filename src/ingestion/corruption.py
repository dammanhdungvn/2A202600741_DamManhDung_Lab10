from __future__ import annotations

import pandas as pd
from core.utils import write_json

from ingestion.crossref import PaperRecord

def build_unprocessed_dataframe(records: list[PaperRecord], output_log_path) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()
        
    df = pd.DataFrame([r.__dict__ for r in records])
    
    # Giữ nguyên cấu trúc thô để Index không bị crash schema
    df['published_dt'] = df['published']
    df['age_days'] = 0
    df['authors_joined'] = df['authors'].apply(lambda x: str(x) if isinstance(x, list) else "")
    df['categories_joined'] = df['categories'].apply(lambda x: str(x) if isinstance(x, list) else "")
    df['summary_chars'] = df['summary'].str.len().fillna(0)
    
    import random
    import json
    
    def simulate_pipeline_failure(row):
        rand = random.random()
        # 1. Lỗi bị chặn cào dữ liệu (Scraper Blocked - 403 Forbidden HTML)
        if rand < 0.35:
            return f"<!DOCTYPE html><html lang='en'><head><title>403 Forbidden</title></head><body><h1>Access Denied</h1><p>Your IP has been blocked by Cloudflare.</p><!-- metadata: {row.get('paper_id')} --></body></html>"
        # 2. Lỗi cấu trúc JSON thay đổi (Schema Drift / Parsing Error)
        elif rand < 0.70:
            return f"{{'status': 500, 'error': 'Failed to parse abstract', 'raw_dump': {json.dumps(row.get('title', ''))}, 'body': '[Object object]'}}"
        # 3. Lỗi mất mát dữ liệu (Null propagation)
        else:
            title_trunc = str(row.get('title', ''))[:20]
            return f"NaN | NULL | {title_trunc}... | NaN | NoneType object has no attribute 'abstract'"

    # Mô phỏng tập Bẩn (Corrupted) bằng các lỗi Pipeline thực tế
    df['text_for_embedding'] = df.apply(simulate_pipeline_failure, axis=1)
    
    write_json(output_log_path, ["Giả lập các lỗi Data Pipeline thực tế (403 HTML, JSON Schema Drift, Null Propagation) vào tập Dữ liệu Bẩn."])
    return df
