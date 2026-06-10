# Project Architecture (Lab 10 MVP)

This document outlines the directory structure and module responsibilities for the Data Pipeline and Observability project.

## Directory Tree

```text
Day-10-Data-Pipeline-Data-Observability/
├── data/                       # Local storage for all artifacts (Git-ignored)
│   ├── raw/                    # Raw JSON responses from Crossref API
│   ├── clean/                  # Cleaned datasets ready for embeddings
│   ├── embeddings/             # Local ChromaDB vector storage
│   ├── eval/                   # Testset questions and ground truths
│   ├── results/                # Evaluation results (Metrics, hit rates)
│   ├── quality/                # Observability logs (null rates, schema checks)
│   └── reports/                # Final Markdown comparison reports
├── docs/                       # Project documentation (PRD, TechDesign, Architecture)
├── agent_docs/                 # Context files specifically optimized for AI Agents
├── script/                     # Entry points for execution
│   ├── run_phase1.py           # Baseline execution script
│   └── run_corruption_flow.py  # Degradation and repair execution script
├── src/                        # Main source code
│   ├── core/                   # Core utilities
│   │   ├── config.py           # Environment variables & constants
│   │   └── logger.py           # Centralized logging configuration
│   ├── ingestion/              # Data extraction and transformation
│   │   ├── crossref.py         # API calls to Crossref
│   │   ├── cleaning.py         # Text normalization and feature extraction
│   │   └── corruption.py       # Simulating data errors (stale, duplicate, null)
│   ├── retrieval/              # RAG and Vector store logic
│   │   ├── embeddings.py       # all-MiniLM-L6-v2 logic
│   │   ├── index.py            # ChromaDB management
│   │   ├── llm.py              # Multi-provider LLM abstraction
│   │   ├── qa.py               # Question answering logic
│   │   └── agent.py            # Orchestrator for retrieval + generation
│   ├── evaluation/             # System measurement
│   │   ├── testset.py          # Generation of golden testset
│   │   └── metrics.py          # Hit rate, F1 score, LLM-as-a-judge calculations
│   ├── observability/          # Data monitoring
│   │   ├── quality.py          # Schema validation and freshness rules
│   │   └── reporting.py        # Report generation
│   └── pipelines/              # High-level pipeline flows
│       ├── phase1.py           # Baseline pipeline orchestrator
│       └── corruption_flow.py  # Corruption pipeline orchestrator
├── tests/                      # Unit tests (pytest)
├── .env                        # Environment variables (Secrets, config)
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview
```

## Module Responsibilities
- **`src/ingestion`**: Focuses purely on ETL. Extracts data, applies deterministic transformations, and ensures output schema matches expectations.
- **`src/retrieval`**: Handles the AI logic. Embedding the text, semantic search, and prompt engineering for the Qwen model.
- **`src/observability`**: Acts as the gatekeeper. It must throw warnings or block the pipeline if data quality drops below thresholds.
- **`src/pipelines`**: Glues the above components together into chronological, repeatable workflows.
