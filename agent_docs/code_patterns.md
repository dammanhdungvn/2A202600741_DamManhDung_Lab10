# Code Patterns & Guidelines

- **Environment Isolation:** Ensure all execution context expects `source ./venv/bin/activate`.
- **Configuration:** Use `python-dotenv` to load `.env` from the project root.
- **Fail Fast:** If required environment variables (e.g., `QWEN_API_KEY`, `QWEN_BASE_URL`) are missing, raise a `ValueError` immediately. Do not silently fallback.
- **LLM Integration:** Use the standard `OpenAI` client initialized with custom `base_url` and `api_key` for Qwen. Do not hardcode these.
- **Modularity:** Separate concerns. `src/ingestion/` handles fetching and cleaning. `src/retrieval/` handles embedding and generation. `src/observability/` handles metrics.
- **Idempotency:** When upserting to ChromaDB, use a unique identifier (like Crossref DOI) to avoid duplicate documents on multiple runs.
