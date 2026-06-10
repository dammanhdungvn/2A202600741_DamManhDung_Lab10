from __future__ import annotations

from datetime import datetime, UTC
import pandas as pd

from ingestion.crossref import PaperRecord
from core.utils import normalize_whitespace

def build_clean_dataframe(records: list[PaperRecord], run_date: datetime) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()
        
    df = pd.DataFrame([r.__dict__ for r in records])
    
    df['title'] = df['title'].apply(normalize_whitespace)
    df['summary'] = df['summary'].apply(normalize_whitespace)
    df['summary'] = df['summary'].fillna("")
    
    df['published_dt'] = pd.to_datetime(df['published'], errors='coerce', utc=True)
    
    df['age_days'] = (run_date - df['published_dt']).dt.days
    df['age_days'] = df['age_days'].fillna(0).astype(int)
    
    df['authors_joined'] = df['authors'].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")
    df['categories_joined'] = df['categories'].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")
    df['summary_chars'] = df['summary'].str.len()
    
    df['text_for_embedding'] = "Title: " + df['title'] + "\nAuthors: " + df['authors_joined'] + "\nAbstract: " + df['summary']
    
    df = df.drop_duplicates(subset=['paper_id'])
    df = df[(df['title'] != "") & (df['summary'] != "")]
    
    df = df.sort_values(by='published_dt', ascending=False)
    df['published_dt'] = df['published_dt'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    return df
