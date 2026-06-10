from __future__ import annotations

import pandas as pd
from core.utils import write_json

def corrupt_clean_dataframe(df: pd.DataFrame, output_log_path) -> pd.DataFrame:
    df_corrupt = df.copy()
    if len(df_corrupt) == 0:
        return df_corrupt
        
    logs = []
    
    # 1. Blank summary
    if len(df_corrupt) >= 1:
        idx = df_corrupt.index[0]
        df_corrupt.at[idx, 'summary'] = ""
        df_corrupt.at[idx, 'summary_chars'] = 0
        logs.append(f"Blanked summary at index {idx}")
        
    # 2. Add duplicate rows
    if len(df_corrupt) >= 2:
        dup_row = df_corrupt.iloc[[1]].copy()
        df_corrupt = pd.concat([df_corrupt, dup_row], ignore_index=True)
        logs.append(f"Duplicated row with paper_id {dup_row['paper_id'].values[0]}")
        
    # 3. Make published date old (stale)
    if len(df_corrupt) >= 3:
        idx = df_corrupt.index[2]
        old_date = pd.Timestamp.now() - pd.Timedelta(days=1000)
        df_corrupt.at[idx, 'published_dt'] = old_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        df_corrupt.at[idx, 'age_days'] = 1000
        logs.append(f"Made published date stale for index {idx}")
        
    # Rebuild text_for_embedding
    df_corrupt['text_for_embedding'] = df_corrupt.apply(
        lambda row: f"Title: {row.get('title', '')}\nAuthors: {row.get('authors_joined', '')}\nPublished: {row.get('published', '')}\nCategories: {row.get('categories_joined', '')}\nSummary: {row.get('summary', '')}",
        axis=1
    )
    
    write_json(output_log_path, logs)
    return df_corrupt
