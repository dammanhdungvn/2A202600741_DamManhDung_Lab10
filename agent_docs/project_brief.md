# Project Brief

This project is a Lab assignment (Lab 10) focused on Data Pipeline & Data Observability for a RAG system. The goal is to ingest scholarly papers from the Crossref API, transform them into a clean format, chunk them, embed them, and make them searchable via a local ChromaDB instance. 

Crucially, the system must implement Data Observability (Quality Gates & Freshness Monitoring) to ensure that the LLM agent (powered by Qwen via OpenAI compatible API) only answers based on high-quality data. A corruption simulation flow will be built to prove that corrupted data degrades performance, and that the repair flow can restore it.
