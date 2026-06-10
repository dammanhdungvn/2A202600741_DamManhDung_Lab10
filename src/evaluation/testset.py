from __future__ import annotations

from typing import Any
import pandas as pd
from core.utils import write_json

def build_test_set(df: pd.DataFrame, output_path) -> list[dict[str, Any]]:
    if len(df) == 0:
        return []
    
    # Giảm xuống 1 để tăng tốc độ chạy Pipeline (test 3 câu hỏi thay vì 15)
    sample_df = df.head(1)
    
    test_set = []
    for idx, row in sample_df.iterrows():
        test_set.append({
            "id": f"q_summary_{row['paper_id']}",
            "question_type": "summary",
            "question": f"What is the summary of the paper titled '{row['title']}'?",
            "ground_truth": row.get('summary', ''),
            "ground_truth_doc_ids": [row['paper_id']]
        })
        
        test_set.append({
            "id": f"q_authors_{row['paper_id']}",
            "question_type": "authors",
            "question": f"Who authored the paper titled '{row['title']}'?",
            "ground_truth": row.get('authors_joined', ''),
            "ground_truth_doc_ids": [row['paper_id']]
        })
        
        test_set.append({
            "id": f"q_date_{row['paper_id']}",
            "question_type": "date",
            "question": f"When was the paper titled '{row['title']}' published?",
            "ground_truth": str(row.get('published', '')),
            "ground_truth_doc_ids": [row['paper_id']]
        })

    write_json(output_path, test_set)
    return test_set
