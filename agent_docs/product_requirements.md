# Product Requirements

Please refer directly to the detailed PRD: `docs/PRD-Lab10-MVP.md`

**Key Requirements Summary:**
1. **Ingestion:** Fetch JSON from `api.crossref.org/works`.
2. **Cleaning:** Transform data, create `text_for_embedding`, calculate `age_days`.
3. **Indexing:** Store embeddings in local ChromaDB using `all-MiniLM-L6-v2`.
4. **Agent:** Answer questions strictly based on context with citations `[Source, Year]`.
5. **Observability:** Monitor data schema, null rates, uniqueness, and freshness.
6. **Evaluation:** Run baseline metrics (`retrieval_hit_rate`, `mean_token_f1`, LLM-as-a-judge).
7. **Simulation:** Corrupt the data intentionally, measure degradation, repair, and output comparison reports.
