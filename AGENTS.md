# Agent Master Plan

## Project Overview
- **Name:** Lab 10 - Data Pipeline & Data Observability
- **Goal:** Build an end-to-end data pipeline (ingest, clean, embed, store) and RAG system with Data Observability to prevent "Garbage in → Garbage out".
- **Tech Stack:** Python 3, ChromaDB, sentence-transformers, OpenAI SDK (Qwen via compatible API), pandas.
- **Current Phase:** Building MVP Phase.

## How I Should Think
- **Understand:** Read the context files in `agent_docs/` and project documents (`docs/`) to understand the requirements and constraints.
- **Ask:** If anything is ambiguous or contradictory, stop and ask the user. Do not assume.
- **Plan:** Before writing code, briefly explain the implementation plan.
- **Verify:** After writing code, verify that it adheres to the architecture, environment requirements (`.venv`), and `.env` specifications.
- **Explain:** Summarize what was done and what remains.

## Workflow
Plan -> Execute -> Verify

## Context Files
- `docs/PRD-Lab10-MVP.md`: Product Requirements
- `docs/TechDesign-Lab10-MVP.md`: Technical Architecture
- `agent_docs/tech_stack.md`: Tech stack details
- `agent_docs/code_patterns.md`: Coding guidelines
- `agent_docs/testing.md`: Testing strategy
- `docs/qwen-api.md`: LLM API constraints

## Roadmap
- [x] **Phase 1:** Setup Ingestion (Crossref API) & Data Cleaning.
- [x] **Phase 2:** Build Indexing (ChromaDB + MiniLM).
- [x] **Phase 3:** Develop QA Agent with multi-provider LLM (Qwen).
- [x] **Phase 4:** Implement Evaluation (testset, metrics) and Observability gates.
- [ ] **Phase 5:** Build and run Corruption & Repair Flow to validate observability.

## What NOT To Do
- **DO NOT** hardcode secrets or base URLs. Always read from `.env` using `os.getenv()`.
- **DO NOT** run scripts outside of the virtual environment. Always instruct the user or assume `source ./venv/bin/activate` is run.
- **DO NOT** use `os.environ.get()` with fallbacks to hardcoded secrets. Fail fast if environment variables are missing.
- **DO NOT** change the `all-MiniLM-L6-v2` embedding model or `ChromaDB` without user approval.
- **DO NOT** modify the `.env` file structure without asking.
