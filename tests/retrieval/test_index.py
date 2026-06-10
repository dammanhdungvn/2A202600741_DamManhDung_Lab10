import pandas as pd
from unittest.mock import MagicMock
from retrieval.index import LocalEmbeddingIndex

def test_local_embedding_index_build_and_search(tmp_path):
    # Mock settings to avoid frozen dataclass issues and use tmp_path
    settings = MagicMock()
    settings.paths.chroma_dir = tmp_path / "chroma"
    settings.paths.embeddings_json = tmp_path / "embeddings.json"
    settings.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
    settings.baseline_collection_name = "test_collection"
    settings.top_k = 1
    
    df = pd.DataFrame([
        {
            "paper_id": "doi1",
            "title": "Quantum Computing",
            "published": "2023",
            "authors_joined": "Alice",
            "categories_joined": "Physics",
            "summary": "About quantum states.",
            "abs_url": "",
            "pdf_url": "",
            "text_for_embedding": "Quantum Computing. About quantum states."
        },
        {
            "paper_id": "doi2",
            "title": "Machine Learning",
            "published": "2024",
            "authors_joined": "Bob",
            "categories_joined": "CS",
            "summary": "About neural networks.",
            "abs_url": "",
            "pdf_url": "",
            "text_for_embedding": "Machine Learning. About neural networks."
        }
    ])
    
    # 1. Test Build
    index = LocalEmbeddingIndex.build(df, settings, embeddings_output_path=settings.paths.embeddings_json)
    
    assert settings.paths.embeddings_json.exists()
    assert (tmp_path / "chroma").exists()
    assert index.collection.count() == 2
    
    # 2. Test Search
    results = index.search("quantum")
    assert len(results) == 1
    assert results[0].paper_id == "doi1"
    
    # 3. Test Idempotency (re-build should drop collection and recreate)
    index2 = LocalEmbeddingIndex.build(df, settings, embeddings_output_path=settings.paths.embeddings_json)
    assert index2.collection.count() == 2
