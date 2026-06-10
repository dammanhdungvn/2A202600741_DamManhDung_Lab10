# Technical Design Document: Data Pipeline & Data Observability MVP (Lab 10)

## 1. Recommended Approach
**Architecture Pattern:** Modular ETL Pipeline + RAG System with Observability Layer.
- **ETL:** Batch processing using plain Python scripts to extract data from the Crossref API, clean it, and load it into ChromaDB.
- **RAG Agent:** Uses the OpenAI SDK in compatible mode to interface with the Qwen LLM (`qwen3.5-flash`), with `sentence-transformers/all-MiniLM-L6-v2` for embeddings.
- **Observability:** Custom Python modules implementing data quality gates (schema validation, null checks) and freshness monitoring.

## 2. Alternative Options
- **ETL Orchestration:** Airflow or Prefect. *Rejected* for MVP due to overhead; a cron-style or simple Python script is sufficient.
- **Vector DB:** Pinecone or Weaviate. *Rejected* because ChromaDB allows for local, serverless execution without network latency or API costs.
- **LLM:** OpenAI GPT-4. *Rejected* in favor of Qwen (`qwen3.5-flash`) via DashScope compatible API to save costs and meet project requirements, though the design uses the OpenAI SDK, allowing an easy swap in the future.

## 3. Project Setup
- **Environment:** Local Python Virtual Environment (`python3 -m venv .venv`). **Must** be activated via `source ./venv/bin/activate` prior to running scripts.
- **Dependencies:** Managed via `requirements.txt`. Key libraries: `requests`, `pandas`, `chromadb`, `sentence-transformers`, `openai`, `python-dotenv`.
- **Environment Variables (`.env`):**
  - `LLM_PROVIDER=qwen`
  - `LLM_MODEL=qwen3.5-flash`
  - `QWEN_API_KEY`, `QWEN_BASE_URL` (configured for OpenAI SDK compatible mode).
- **Core Scripts:** 
  - `script/run_phase1.py` (Baseline ETL & Evaluation)
  - `script/run_corruption_flow.py` (Observability, Degradation & Repair testing)

## 4. Feature Implementation
### 4.1 Ingestion (`src/ingestion/crossref.py`)
- Call `https://api.crossref.org/works`.
- Handle JSON parsing: extract `DOI`, `title`, `author`, `issued`, etc.
- Implement rate limiting / polite pool logic.

### 4.2 Cleaning & Corruption (`src/ingestion/cleaning.py` & `src/ingestion/corruption.py`)
- **Cleaning:** Drop invalid records, normalize strings, calculate `age_days` for freshness. Build `text_for_embedding` using a combination of `title`, `summary`, and `authors`.
- **Corruption:** Expose functions to delete recent records, empty strings, and duplicate rows to simulate real-world failure.

### 4.3 Agent & QA (`src/retrieval/agent.py`)
- Initialize `OpenAI` client using `os.getenv("QWEN_API_KEY")` and `base_url=os.getenv("QWEN_BASE_URL")`.
- Implement `generate_answer(question, contexts)` enforcing strict rules:
  - Cite sources `[Source, Year]`.
  - Fallback: "I cannot verify this information" if context is insufficient.

### 4.4 Observability (`src/observability/quality.py` & `reporting.py`)
- **Quality Gates:** Verify schema constraints (e.g., `text_for_embedding` is not empty, `DOI` is unique).
- **Evaluation:** Measure Token F1 score and Hit Rate, plus an LLM-as-a-judge mechanism.
- **Reporting:** Auto-generate Markdown reports summarizing metrics baseline vs. corrupted.

## 5. Database & Storage
- **Local Artifacts:**
  - `data/raw/`: Raw Crossref JSON responses.
  - `data/clean/`: Cleaned dataset files.
  - `data/results/` & `data/reports/`: Evaluation outputs.
- **Vector Storage:** ChromaDB running locally (`data/embeddings/`), using `sentence-transformers/all-MiniLM-L6-v2`.

## 6. AI Assistance Strategy
- **Prompt Engineering:** Use strict system prompts for Qwen to prevent hallucinations and enforce citation formats.
- **Evaluation:** Utilize LLM-as-a-judge to grade generated answers against ground-truth references.

## 7. Deployment Plan
- **Current MVP:** Local execution only. Scripts are run manually via the terminal after activating `.venv`.
- **Future:** Containerize using Docker; deploy the ETL as a cron job on a cloud VM; expose the QA agent via a FastAPI endpoint.

## 8. Cost Breakdown
- **Compute:** Local machine ($0).
- **Vector DB:** ChromaDB local ($0).
- **LLM API:** Qwen API (`qwen3.5-flash`) - minimal cost or free tier. Crossref API ($0).
- **Total MVP Cost:** ~$0.

## 9. Scaling Path
1. Replace local Python scripts with Apache Airflow or Prefect for robust DAG orchestration.
2. Migrate local ChromaDB to a managed vector database (e.g., Pinecone).
3. Scale the ingestion to process millions of papers using distributed processing.
4. Implement a user-facing UI with Streamlit or Next.js.

## 10. Limitations
- **Local Bottleneck:** ChromaDB and MiniLM embeddings run locally; performance depends on the host machine hardware.
- **API Rate Limits:** Crossref API is rate-limited; ingestion might be slow for large datasets.
- **Idempotency Challenges:** File-based tracking might cause duplicate embeddings if not explicitly handled with upserts in ChromaDB.
