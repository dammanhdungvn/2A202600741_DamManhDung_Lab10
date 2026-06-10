import pytest
import pandas as pd
from datetime import datetime, UTC
from ingestion.crossref import PaperRecord
from ingestion.cleaning import build_clean_dataframe

def test_build_clean_dataframe():
    now = datetime(2024, 1, 1, tzinfo=UTC)
    records = [
        PaperRecord(
            paper_id="doi1", title="  Test Title 1 ", summary="Summary 1",
            authors=["A", "B"], categories=["AI"], primary_category="AI",
            published="2023-12-01T00:00:00Z", updated="", abs_url="", pdf_url="", comment=""
        ),
        PaperRecord(
            paper_id="doi2", title="", summary="Empty title should be removed",
            authors=[], categories=[], primary_category="",
            published="2023-12-01T00:00:00Z", updated="", abs_url="", pdf_url="", comment=""
        ),
        PaperRecord( # Duplicate
            paper_id="doi1", title="Test Title 1", summary="Summary 1",
            authors=["A", "B"], categories=["AI"], primary_category="AI",
            published="2023-12-01T00:00:00Z", updated="", abs_url="", pdf_url="", comment=""
        )
    ]
    
    df = build_clean_dataframe(records, run_date=now)
    
    assert len(df) == 1
    assert df.iloc[0]["paper_id"] == "doi1"
    assert df.iloc[0]["title"] == "Test Title 1" # Strip whitespace
    assert df.iloc[0]["age_days"] == 31
    assert "Title: Test Title 1" in df.iloc[0]["text_for_embedding"]
