# 📚 Day 10 — Data Pipeline & Data Observability
> **Khóa học:** AICB-P1 · VinUniversity · Phase 1 · 2026  
> **Chủ đề:** Garbage in → garbage out — fix thế nào?

---

## 🧭 Tổng quan bài học

| # | Chủ đề |
|---|--------|
| 1 | Data Pipeline Fundamentals |
| 2 | Ingestion — Thu thập data từ nhiều nguồn |
| 3 | Transform — Làm sạch & chuẩn hóa data |
| 4 | Data Quality — 6 Dimensions |
| 5 | Data Observability |
| 6 | ETL Automation & Orchestration |

---

## 1. Data Pipeline Fundamentals

### Tại sao Data Pipeline là nền tảng của mọi AI product?
- **60–80% thời gian** trong AI project thực tế là **data work**, không phải model
- Tỷ lệ thực tế: 20% xây model/agent — 80% data collection, cleaning, pipeline, monitoring
- RAG agent xuất sắc vẫn **hallucinate** nếu vector store được nạp data bẩn
- **Garbage in → Garbage out**: output quality tỷ lệ thuận với input data quality
- **Observability** = cơ chế phát hiện data sai **trước khi user phàn nàn**

### Data Pipeline là gì?
> Chuỗi các bước **tự động hóa** việc thu thập, xử lý, và phân phối data từ nguồn đến đích

**AI Data Stack điển hình:**
```
Sources → Pipeline → Storage → Serving → Agent
```
- **Sources:** DB, API, files, streams
- **Pipeline:** ingest + transform
- **Storage:** warehouse, vector store
- **Serving:** API, cache layer
- **Agent:** LLM + tools + RAG

### Pipeline cho AI khác BI ở điểm nào?
| BI sai | Agent sai |
|--------|-----------|
| Số sai trên báo cáo | Hành động hoặc trả lời sai trực tiếp với user |

Pipeline cho AI cần thêm: **chunking, metadata, embeddings, retrieval checks, trace logs**

### Điểm fail trong pipeline RAG nội bộ:
- **Ingestion fail** → tài liệu mới không vào store → agent trả lời cũ
- **Transform sai** → chunk xấu, metadata thiếu → retrieve nhầm
- **Index lỗi** → embed thiếu hoặc duplicate → context méo

---

### ETL vs. ELT

| | ETL (Extract → Transform → Load) | ELT (Extract → Load → Transform) |
|--|--|--|
| **Cách hoạt động** | Transform trước khi load | Load raw data, transform sau trong kho |
| **Phù hợp** | Data nhạy cảm, cần mask trước khi lưu | Big data, cloud data warehouses |
| **Ví dụ** | Redact PII trong ticket support trước khi embed | Load raw docs/logs trước, rồi chunk + enrich trong lakehouse |
| **Tools** | Talend, Informatica, custom scripts | Spark SQL, BigQuery, custom Python jobs |

**Thực tế:** Nhiều team dùng **hybrid** — load raw trước, nhưng ETL các phần nhạy cảm (PII, secrets, dữ liệu pháp lý) trước khi index hoặc serve cho agent.

**Chọn ETL nếu:** cần mask PII trước · schema ổn định · data vào agent phải rất sạch · muốn giảm rủi ro lưu raw nhạy cảm

**Chọn ELT nếu:** nhiều nguồn, nhiều định dạng · phải backfill/replay thường xuyên · còn thử chunking, labeling, feature engineering · cần giữ raw cho audit và experiment

---

### Batch vs. Streaming

| | Batch Processing | Streaming Processing |
|--|--|--|
| **Cơ chế** | Xử lý theo lô, theo lịch (hourly/daily) | Xử lý realtime khi data xuất hiện |
| **Ưu** | Đơn giản, cost thấp, dễ debug | Latency thấp (ms–giây) |
| **Nhược** | Latency cao (data trễ vài giờ) | Phức tạp hơn, cost cao hơn |
| **Dùng khi** | Training data, daily reports, ETL | Fraud detection, live agent context |

---

## 2. Ingestion — Thu Thập Data Từ Nhiều Nguồn

### Các loại nguồn data phổ biến

**Structured sources:**
- Databases (PostgreSQL, MySQL): CDC để capture changes
- Data warehouses: Snowflake, BigQuery
- REST / GraphQL APIs: rate limits cần xử lý

**Unstructured sources:**
- Files: CSV, JSON, Parquet, PDF, Word
- Object storage: S3, GCS, Azure Blob
- Web scraping: HTML → text extraction

**Event streams:**
- Kafka / Kinesis: high-throughput event bus
- Webhooks: push từ external services
- IoT sensors: time-series data

> **CDC (Change Data Capture):** Detect & capture mọi INSERT/UPDATE/DELETE trong database để sync realtime thay vì full scan

### Ingestion trong hệ AI/Agentic

**Nguồn data thường lấy từ:**
- **Knowledge sources:** Notion, Confluence, PDF, Word, SharePoint
- **Transactional data:** CRM, ticketing, order DB, HR systems
- **Logs + feedback:** chat transcripts, tool calls, thumbs up/down, escalation notes

**Thiết kế ingestion tốt cần:**
- **Incremental sync:** chỉ lấy phần changed since last run
- **Idempotent upsert:** chạy lại không tạo duplicate chunks
- **Source versioning:** biết bản nào mới nhất, sync lúc nào

**Patterns xử lý lỗi:**
- **Rate limiting:** exponential backoff khi API giới hạn req/min
- **Backpressure:** buffer hoặc pause signal khi consumer xử lý chậm hơn producer
- **Retry logic:** dead-letter queue cho failed records

### Checklist ingestion cho AI:
1. Có lấy **đúng nguồn** không?
2. Có lấy **đủ bản mới nhất** không?
3. Có biết record nào **thất bại** không?
4. Có log được **run ID** và thời gian sync không?

---

## 3. Transform — Làm Sạch & Chuẩn Hóa Data

### Data Cleaning — Các vấn đề phổ biến
- **Missing values:** NULL, empty string, "N/A" → drop, impute, hoặc flag
- **Outliers:** giá trị bất thường ảnh hưởng embedding quality
- **Duplicates:** dedup bằng hash hoặc fuzzy match
- **Wrong formats:** standardize date, number format
- **Encoding issues:** luôn enforce UTF-8

### Text normalization cho AI:
- **Lowercasing:** tùy model, không phải lúc nào cũng cần
- **Unicode normalization:** NFC/NFD cho tiếng Việt
- **Whitespace:** collapse multiple spaces, strip trailing
- **HTML stripping:** loại bỏ tags trước khi embed
- **Language detection:** tách chunks theo ngôn ngữ
- **Schema validation:** reject records không đúng schema thay vì để lọt vào model

### Transform cho AI/RAG khác BI:
> BI thường transform để báo cáo; AI transform để model **hiểu đúng ngữ cảnh** và **retrieve đúng evidence**

**Các bước transform thường gặp trong AI:**
1. **Clean text:** bỏ HTML, ký tự lỗi, OCR noise
2. **Chunking:** chia tài liệu thành đoạn vừa ngữ nghĩa, vừa token budget
3. **Metadata enrichment:** gắn source, owner, version, effective date
4. **Redaction:** loại PII/secrets trước khi embed
5. **Canonicalization:** chuẩn hóa tên sản phẩm, mã đơn hàng, timestamp

### Chunking & Metadata

| Chunk quá to | Chunk quá nhỏ |
|--|--|
| Nhiều chủ đề → retrieval mơ hồ | Mất context quan trọng |
| Tốn token, giảm chỗ cho reasoning | Câu trả lời thiếu điều kiện hoặc ngoại lệ |

**Chunk tốt thường cần:**
```
content · chunk_id · source_doc_id · section/title
effective_date · owner/department · version/updated_at
```

> ⚠️ **Lưu ý:** Nhiều team chỉ embed "text thuần" mà quên metadata → retrieve được đoạn đúng nhưng không biết nó đến từ bản policy nào.

---

## 4. Data Quality — 6 Dimensions

| Dimension | Định nghĩa | Cách check |
|-----------|------------|-----------|
| **1. Completeness** | Không thiếu records hoặc fields quan trọng | % NULL, row count so với expected |
| **2. Accuracy** | Data đúng với thực tế | Validate với nguồn gốc, business rules |
| **3. Consistency** | Cùng entity, cùng format across systems | Cross-system reconciliation |
| **4. Timeliness** | Data đủ fresh cho use case | Max age, last-updated timestamp |
| **5. Validity** | Data theo đúng format và domain rules | Regex patterns, range checks |
| **6. Uniqueness** | Không có duplicates | Dedup rate, composite key uniqueness |

### Quality Gates trước khi data đến Agent

> Trong AI pipeline, data quality không chỉ bảo vệ warehouse mà còn bảo vệ **retrieval, tool use** và **final answer**

**Các quality gates nên có:**
- **Schema gate:** có đủ content, doc_id, updated_at
- **Freshness gate:** policy quá cũ thì reject hoặc cảnh báo
- **Content gate:** text đủ dài, OCR confidence không quá thấp
- **Dedup gate:** cùng chunk không được nạp nhiều lần
- **PII gate:** không embed số thẻ, mật khẩu, access token

### Data issue → Agent symptom mapping

| Data Issue | Agent Symptom |
|-----------|--------------|
| Missing documents | Không tìm thấy bằng chứng liên quan |
| Outdated version | Trả lời dựa trên policy cũ |
| Duplicate chunks | Lặp lại cùng một ý nhiều lần |
| Wrong metadata | Cite sai phòng ban / sai ngày hiệu lực |
| Secret leakage | Làm lộ dữ liệu nhạy cảm cho user |

> 🔑 **Điểm quan trọng:** Nhiều lỗi nhìn giống "model hallucination" nhưng gốc rễ thực ra là **data pipeline bug**.

---

## 5. Data Observability

### 5 Pillars of Data Observability

| Pillar | Câu hỏi |
|--------|---------|
| **Freshness** | Data có đang được update theo đúng lịch? |
| **Distribution** | Giá trị phân phối có bất thường không? (null rate, range) |
| **Volume** | Số lượng records tăng/giảm bất thường? |
| **Schema** | Cột bị đổi tên, thêm, xóa không? |
| **Lineage** | Data đến từ đâu, đi qua transform nào? |

**Data Lineage:** Track hành trình data từ nguồn gốc → pipeline → chunk/index → retrieved context → model output

### Muốn debug được, phải log ít nhất:
- question / session ID
- retrieved chunk IDs
- source document version
- embedding/index version
- pipeline run ID

### Debug Agent Sai — Trace 5 lớp từ output ngược về data:
1. **Output layer:** agent trả lời gì, cite gì, confidence ra sao?
2. **Retrieval layer:** top-k chunks nào được lấy ra? có zero-hit không?
3. **Index layer:** chunk đó được embed bằng model/version nào?
4. **Pipeline layer:** run nào sinh ra chunk? pass/fail quality gates nào?
5. **Source layer:** tài liệu gốc có đúng, mới và đầy đủ không?

> ⚠️ Nếu chỉ nhìn final answer mà không trace được về chunk và source document → **đang debug trong bóng tối**.

### Monitoring metrics cần theo dõi:
- **Pipeline SLA:** % runs hoàn thành đúng giờ
- **Row count delta:** ∆ records qua các runs
- **Null rate per column:** alert nếu tăng đột biến
- **Schema drift:** tự động detect column changes
- **Data freshness:** max age của records trong store
- **Embedding coverage:** % chunks đã được embed

### Observability cho Agentic Systems (2 loại signals):

**Pipeline / data signals:**
- Freshness của knowledge base
- Failed sync count, dead-letter queue size
- Duplicate chunk rate, missing metadata rate
- Embedding queue lag

**Agent / product signals:**
- Retrieval hit rate
- % answers có citation hợp lệ
- User correction / escalation rate
- Tool-call failure rate
- Abandoned conversations sau câu trả lời sai

> **Quan điểm thực chiến:** Observability tốt phải nối được **data issue → retrieval issue → business impact**.

---

## 6. ETL Automation & Orchestration

### Apache Airflow — DAG-Based Orchestration

**Core concepts:**
- **DAG** (Directed Acyclic Graph): định nghĩa thứ tự task
- **Operator:** đơn vị thực thi (PythonOperator, BashOperator, ...)
- **Scheduler:** trigger DAGs theo cron hoặc event
- **Executor:** chạy tasks (Local, Celery, Kubernetes)
- **XCom:** truyền data nhỏ giữa tasks

**Dùng Airflow khi:** batch pipeline phức tạp, team có Python skills, cần UI visibility đầy đủ

### So sánh Orchestration tools:

| Tool | Hay dùng cho | Lý do |
|------|-------------|-------|
| **Airflow** | Batch ETL, retraining theo lịch, multi-step jobs | Mature, nhiều operator, UI quen thuộc |
| **Prefect** | Python pipelines, startup teams, flows cần code nhanh | Ít boilerplate, local-to-cloud dễ |
| **Dagster** | Asset-heavy pipelines, lineage rõ, data platform teams | Asset model hợp với tables, features, indexes |

> **Góc nhìn thực tế:** Hệ RAG/agent nhỏ thường bắt đầu bằng **cron + Python**; khi số bước, số nguồn, số team tăng lên thì mới nâng lên Airflow / Prefect / Dagster.

### Pipeline RAG/Agent hoàn chỉnh:
```
Sync docs/API → Quality gate → Chunk + metadata → Embed → Upsert vector store → Smoke test retrieval → Notify/alert
```

**Nguyên tắc vận hành:**
- **Trigger:** mỗi giờ, khi có file mới, hoặc khi policy đổi
- **Fail fast:** quality gate fail thì không cho index tiếp
- **Smoke test:** chạy vài câu hỏi chuẩn để check retrieval
- **Notify:** báo Slack nếu index mới làm hit rate giảm

### Scheduling strategies:
- **Cron-based:** `0 2 * * *` = 2am mỗi ngày — đơn giản, predictable
- **Event-driven:** trigger khi file mới upload hoặc webhook nhận được
- **Dependency-based:** chỉ chạy khi upstream pipeline xong
- **Backfill:** chạy lại pipeline cho historical dates

### Error handling patterns:
- **Retry với backoff:** attempt 1 → 30s → attempt 2 → 2m → ...
- **Dead Letter Queue:** failed records không bị mất, xử lý sau
- **Partial failure:** idempotent tasks để re-run an toàn
- **Alerting:** Slack/email khi pipeline fail
- **SLA breach:** alert khi pipeline trễ so với deadline

> ⚠️ **Idempotency là bắt buộc:** chạy lại pipeline 2 lần phải cho kết quả giống chạy 1 lần. Thiếu idempotency → duplicate data trong vector store.

---

## ✅ Key Takeaways

1. **Data pipeline là hệ tuần hoàn** của mọi AI product — agent mạnh đến đâu cũng vô dụng nếu data vào bị bẩn
2. **Pipeline cho AI khác BI** ở chỗ phải tối ưu cho retrieval, context quality, citations và khả năng debug agent
3. **Data quality gates** phải chặn thiếu dữ liệu, dữ liệu cũ, duplicate chunks, metadata sai và secret leakage
4. **Observability tốt** cho phép trace từ câu trả lời sai ngược về chunk, pipeline run và source document

---

## 📚 Tài liệu tham khảo

1. **Hidden Technical Debt in Machine Learning Systems** — Sculley et al., Google, NeurIPS 2015
2. **Designing Data-Intensive Applications** — Martin Kleppmann
3. **Designing Machine Learning Systems** — Chip Huyen

---

## 🔜 Bài tiếp theo

**Guardrails & AI Safety** — *"Agent hoạt động đúng không có nghĩa là an toàn — cần lớp bảo vệ ở mọi cấp"*

- Đọc: OWASP Top 10 for LLMs (owasp.org)
- Thực hành: Thêm input/output validation vào ETL pipeline từ Lab 10
- Suy nghĩ: Agent của bạn có thể bị poisoned data attack không?

---

## 🧪 Lab #10

**Mục tiêu:** Build AI data pipeline hoàn chỉnh: thu thập raw docs, làm sạch, chunk, enrich metadata, embed và nạp vào vector store cho agent. Simulate data corruption để đo impact lên retrieval và câu trả lời.

**Deliverable:**
1. Pipeline script: raw → cleaned → chunked → embedded
2. Quality gates cho schema/freshness/duplicates
3. Trace log để debug agent answers
4. So sánh response quality trước/sau fix data

**Thời gian:** 4 giờ (Vibe Coding 1.5h + Lab 2.5h)

---

*Source code & labs: github.com/vbi-academy/aicb-phase1*