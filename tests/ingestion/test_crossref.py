import responses
from ingestion.crossref import parse_crossref_payload, fetch_source_records

def test_parse_crossref_payload():
    payload = {
        "message": {
            "items": [
                {
                    "DOI": "10.123/456",
                    "title": ["Test Paper"],
                    "abstract": "<jats:p>Abstract text here.</jats:p>",
                    "author": [{"given": "John", "family": "Doe"}],
                    "subject": ["AI", "ML"],
                    "issued": {"date-parts": [[2023, 5, 12]]}
                }
            ]
        }
    }
    records = parse_crossref_payload(payload)
    assert len(records) == 1
    assert records[0].paper_id == "10.123/456"
    assert records[0].title == "Test Paper"
    assert records[0].summary == "Abstract text here."
    assert records[0].authors == ["John Doe"]
    assert records[0].primary_category == "AI"
    assert records[0].published == "2023-05-12T00:00:00Z"

@responses.activate
def test_fetch_source_records(tmp_path):
    # Mock settings
    class MockPaths:
        raw_api_response = tmp_path / "raw_api_response.json"
        raw_records_json = tmp_path / "raw_records_json.json"
    
    class MockSettings:
        source_query = "AI"
        source_filter = "has-abstract:true"
        max_results = 2
        paths = MockPaths()

    settings = MockSettings()
    
    mock_json = {
        "status": "ok",
        "message": {"items": [{"DOI": "10.111/222", "title": ["Paper 1"]}]}
    }
    
    responses.add(
        responses.GET,
        "https://api.crossref.org/works",
        json=mock_json,
        status=200
    )
    
    records = fetch_source_records(settings)
    assert len(records) == 1
    assert records[0].paper_id == "10.111/222"
    assert settings.paths.raw_api_response.exists()
    assert settings.paths.raw_records_json.exists()
