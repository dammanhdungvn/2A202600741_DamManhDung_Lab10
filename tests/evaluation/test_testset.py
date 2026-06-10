import pandas as pd
from evaluation.testset import build_test_set

def test_build_test_set(tmp_path):
    output_path = tmp_path / "testset.json"
    df = pd.DataFrame([
        {
            "paper_id": "doi1",
            "title": "AI Paper",
            "summary": "This is AI.",
            "authors_joined": "John",
            "published": "2024-01-01"
        }
    ])
    
    test_set = build_test_set(df, output_path)
    
    assert len(test_set) == 3
    assert test_set[0]["question_type"] == "summary"
    assert test_set[0]["ground_truth_doc_ids"] == ["doi1"]
    assert output_path.exists()
