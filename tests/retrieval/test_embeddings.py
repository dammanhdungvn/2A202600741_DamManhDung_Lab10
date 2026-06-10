from retrieval.embeddings import MiniLMEmbeddings

def test_embeddings_dimensions():
    embedder = MiniLMEmbeddings("sentence-transformers/all-MiniLM-L6-v2")
    texts = ["This is a test document.", "Here is another one."]
    
    doc_embs = embedder.embed_documents(texts)
    assert len(doc_embs) == 2
    assert len(doc_embs[0]) == 384
    
    query_emb = embedder.embed_query("Test query")
    assert len(query_emb) == 384
