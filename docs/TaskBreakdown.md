# Project Task Breakdown (Module-by-Module & TDD)

Tài liệu này chia nhỏ dự án thành các task độc lập (có thể giao cho nhiều thành viên trong team). Mỗi task đều bắt buộc phải tuân thủ chuẩn TDD: **Viết Test trước/song song -> Viết Code -> Chạy Pass Test**.

## Phase 1: Core Foundation & Ingestion Layer
- [ ] **Task 1.1: Setup Core Logger & Config**
  - *Mô tả:* Implement `src/core/config.py` và `src/core/logger.py`. Đọc và validate chặt chẽ các biến môi trường từ `.env` (QWEN_API_KEY, LLM_MODEL,...).
  - *TDD:* Viết `tests/core/test_config.py` để đảm bảo hệ thống `Fail Fast` (raise ValueError) khi thiếu `.env`.
- [ ] **Task 1.2: Crossref API Client**
  - *Mô tả:* Implement `src/ingestion/crossref.py`. Gọi API lấy dữ liệu scholarly works. Xử lý timeout, retry logic (Rate limit) và parse JSON ra format chuẩn.
  - *TDD:* Viết `tests/ingestion/test_crossref.py`. Dùng thư viện `responses` hoặc `unittest.mock` để giả lập API Call thành công và thất bại.
- [ ] **Task 1.3: Data Cleaning & Transformation**
  - *Mô tả:* Implement `src/ingestion/cleaning.py`. Chuẩn hóa text (loại bỏ ký tự lạ), gộp cột thành `text_for_embedding`, tính tuổi tài liệu `age_days`.
  - *TDD:* Viết `tests/ingestion/test_cleaning.py`. Đưa vào mock Pandas DataFrame chứa dữ liệu lỗi (null, duplicate) để đảm bảo hàm làm sạch chạy đúng.

## Phase 2: Indexing & Retrieval
- [ ] **Task 2.1: Embedding Generation**
  - *Mô tả:* Implement `src/retrieval/embeddings.py` sử dụng model `sentence-transformers/all-MiniLM-L6-v2`.
  - *TDD:* Viết `tests/retrieval/test_embeddings.py`. Đảm bảo vector đầu ra có độ dài chuẩn (vd: 384 dimensions).
- [ ] **Task 2.2: ChromaDB Vector Store**
  - *Mô tả:* Implement `src/retrieval/index.py`. Lưu embeddings vào ChromaDB. Đảm bảo tính Idempotency (dùng DOI làm ID để chạy nhiều lần không bị duplicate).
  - *TDD:* Viết `tests/retrieval/test_index.py` sử dụng ChromaDB in-memory (ephemeral client) để test luồng upsert và query.

## Phase 3: QA Agent Integration
- [ ] **Task 3.1: Multi-Provider LLM Setup**
  - *Mô tả:* Implement `src/retrieval/llm.py`. Wrap OpenAI SDK, kết nối vào endpoint của Qwen thông qua `.env`.
  - *TDD:* Viết `tests/retrieval/test_llm.py` để mock OpenAI client.
- [ ] **Task 3.2: RAG Agent Orchestration**
  - *Mô tả:* Implement `src/retrieval/agent.py`. Lắp ghép context từ ChromaDB vào prompt cho Qwen. Ép rule phải có citation `[Source, Year]`.
  - *TDD:* Viết `tests/retrieval/test_agent.py` kiểm tra prompt format.

## Phase 4: Data Observability & Evaluation
- [ ] **Task 4.1: Data Quality Gates**
  - *Mô tả:* Implement `src/observability/quality.py`. Check các rule: `text_for_embedding` không được rỗng, DOI không trùng lặp, data không quá cũ (Freshness).
  - *TDD:* Viết `tests/observability/test_quality.py`.
- [ ] **Task 4.2: Evaluation Metrics**
  - *Mô tả:* Implement `src/evaluation/metrics.py`. Tính Retrieval Hit Rate, Token F1 Score và LLM-as-a-judge.
  - *TDD:* Viết `tests/evaluation/test_metrics.py` với các input giả định để verify công thức toán học.

## Phase 5: Pipeline Orchestration & Corruption Simulation
- [ ] **Task 5.1: Data Corruption Simulator**
  - *Mô tả:* Implement `src/ingestion/corruption.py`. Cố tình làm hỏng dữ liệu (xóa dòng, làm rỗng text, thay đổi ngày tháng) để test Observability.
  - *TDD:* Viết `tests/ingestion/test_corruption.py`.
- [ ] **Task 5.2: End-to-End Pipelines**
  - *Mô tả:* Cấu trúc `src/pipelines/phase1.py` và `src/pipelines/corruption_flow.py` để xâu chuỗi tất cả module trên, đồng thời sinh ra Markdown reports.
  - *TDD:* Viết Integration Tests kiểm tra luồng file IO (`data/raw/` -> `data/clean/` -> `data/embeddings/`).
