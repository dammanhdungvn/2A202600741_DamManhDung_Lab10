import pandas as pd
from ingestion.corruption import corrupt_clean_dataframe

def test_corrupt_clean_dataframe(tmp_path):
    log_path = tmp_path / "corrupt_log.json"
    df = pd.DataFrame([
        {"paper_id": "1", "title": "A", "summary": "Sum A", "summary_chars": 5, "published_dt": pd.Timestamp.now(), "age_days": 1},
        {"paper_id": "2", "title": "B", "summary": "Sum B", "summary_chars": 5, "published_dt": pd.Timestamp.now(), "age_days": 1},
        {"paper_id": "3", "title": "C", "summary": "Sum C", "summary_chars": 5, "published_dt": pd.Timestamp.now(), "age_days": 1},
    ])
    
    corrupt_df = corrupt_clean_dataframe(df, log_path)
    
    assert log_path.exists()
    assert len(corrupt_df) == 4
    assert corrupt_df.iloc[0]['summary'] == ""
    assert corrupt_df.iloc[2]['age_days'] == 1000
