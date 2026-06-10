# Product Requirements Document (PRD): Data Pipeline & Data Observability MVP (Lab 10)

## 1. Product Overview
The Lab 10 Data Pipeline & Data Observability MVP is an end-to-end Extract, Transform, Load (ETL) pipeline and Retrieval-Augmented Generation (RAG) evaluation system. It ingests scholarly data from the Crossref API, processes and indexes it into ChromaDB, and uses a multi-provider LLM Agent to answer questions. The system explicitly simulates data corruption to demonstrate the value of data observability in maintaining agent accuracy.

## 2. Target Users
- **AI Engineers & Data Engineers:** Professionals learning or implementing robust data ingestion and monitoring for AI/RAG systems.
- **Instructors/Reviewers:** Evaluators scoring the Lab based on predefined Rubric criteria.

## 3. Problem Statement
In AI projects, "Garbage in → Garbage out" is a critical issue. If a RAG system is fed with corrupted, duplicate, or stale data, the LLM will confidently hallucinate or provide incorrect answers. There is a need for a robust data pipeline that not only processes data but also monitors its quality and freshness (Data Observability) before it reaches the AI Agent.

## 4. User Journey
1. **Execution & Setup:** User activates the virtual environment (`source ./venv/bin/activate`) and ensures dependencies are installed.
2. **Baseline Pipeline:** User runs `script/run_phase1.py`. The system fetches academic papers from Crossref, cleans the text, generates embeddings (MiniLM), and stores them in ChromaDB.
3. **Evaluation:** The Agent answers questions from a generated testset, and the system records baseline metrics (hit rate, F1 score).
4. **Corruption Simulation:** User runs `script/run_corruption_flow.py` which deliberately degrades data (deletes records, adds noise, truncates titles).
5. **Observability & Repair:** The system detects data anomalies (quality/freshness failures), evaluates the degraded Agent, repairs the data, and generates a comparison report showing the impact of data quality on the RAG system.

## 5. MVP Features
- **Raw Data Ingestion:** Integration with Crossref API to fetch and parse scholarly works.
- **Data Transformation:** Text normalization, missing field resolution, and `text_for_embedding` compilation.
- **Vector Indexing:** Embedding generation using `sentence-transformers/all-MiniLM-L6-v2` and storage in ChromaDB.
- **Multi-Provider QA Agent:** A RAG agent capable of using OpenAI, Gemini, Anthropic, OpenRouter, or Ollama to answer queries based on the index.
- **Data Observability Module:** Quality gates (schema adherence, completeness, duplication) and freshness checks.
- **Corruption & Comparison Flow:** Scripts to simulate data corruption, re-evaluate, repair, and generate Markdown reports comparing baseline vs. corrupted performance.

## 6. Success Metrics
- **Pipeline Execution:** 100% successful end-to-end execution of both `run_phase1.py` and `run_corruption_flow.py`.
- **Retrieval Performance:** High `retrieval_hit_rate` and `mean_token_f1` for the baseline dataset.
- **Agent Accuracy:** High `judge_accuracy` and `mean_judge_score` on clean data, with a demonstrable drop on corrupted data.
- **Observability Detection:** 100% detection of simulated data anomalies by the Quality and Freshness gates.
- **Grading:** Score 90-100 points based on the Lab 10 Rubric.

## 7. Design Direction
- **Code Architecture:** Modular design with clean separation of concerns (`src/core`, `src/ingestion`, `src/retrieval`, `src/evaluation`, `src/observability`, `src/pipelines`).
- **Data Flow Visibility:** Clear logging and artifact generation (`data/raw`, `data/clean`, `data/eval`, `data/results`, `data/reports`).
- **Reporting:** Auto-generated, highly readable Markdown reports for metric comparisons.

## 8. Technical Considerations
- **LLM Independence:** The Agent must gracefully abstract API calls to support multiple LLM providers.
- **Idempotency:** The pipeline must be repeatable; running it twice should yield the same vector store state without duplicating chunks.
- **Vector DB:** ChromaDB must run locally and efficiently handle upserts and metadata filtering.

## 9. Constraints
- Must use Python 3 and the provided virtual environment.
- Use `all-MiniLM-L6-v2` for embeddings.
- Vector database is restricted to ChromaDB (local).
- The solution must be self-contained and run locally using the provided project structure.

## 10. Definition of Done
- All modules (`crossref.py`, `cleaning.py`, `testset.py`, `quality.py`, `phase1.py`, `corruption_flow.py`, etc.) are fully implemented.
- `run_phase1.py` runs successfully and outputs baseline evaluation metrics.
- `run_corruption_flow.py` runs successfully, corrupts data, proves metric degradation, repairs data, and generates a final comparison Markdown report.
- The project structure strictly follows the provided `Guide.md` and achieves all points in `Rubric.md`.
