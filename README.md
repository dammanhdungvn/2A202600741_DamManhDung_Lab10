# Day 10 - Data Pipeline And Data Observability 🚀

Chào mừng bạn đến với **Lab Day 10: RAG Data Pipeline & Observability**! 
Dự án này là một minh chứng hoàn chỉnh cho việc xây dựng một hệ thống **Retrieval-Augmented Generation (RAG)** không chỉ dừng lại ở mức "chạy được", mà còn được trang bị **Data Observability** (Khả năng quan sát dữ liệu) để kiểm soát chất lượng đầu vào và đầu ra, tuân thủ nguyên lý: **"Garbage In -> Garbage Out"**.

---

## 🎯 1. Idea (Ý tưởng & Mục tiêu)

Mục tiêu của dự án là xây dựng một **ETL Pipeline End-to-End** dành cho hệ thống RAG với các tính năng sau:
- **Ingestion**: Lấy dữ liệu bài báo học thuật thực tế từ Crossref API.
- **Transformation (Cleaning)**: Làm sạch, chuẩn hóa văn bản, xử lý các trường dữ liệu thiếu (missing values).
- **Embedding & Storage**: Vector hóa nội dung bằng `sentence-transformers/all-MiniLM-L6-v2` và lưu trữ cục bộ vào `ChromaDB`.
- **QA Agent**: Tích hợp mô hình ngôn ngữ lớn (LLM - Qwen thông qua API tương thích OpenAI) để trả lời các câu hỏi dựa trên ngữ cảnh được truy xuất (Retrieval).
- **Data Observability & Evaluation**: 
  - Tự động sinh Testset từ dữ liệu (LLM-based test generation).
  - Đánh giá chất lượng RAG qua **LLM-as-a-judge** với các tiêu chí: *Context Precision*, *Answer Relevance*, *Context Recall*.
  - Đo lường độ chính xác (Accuracy) và Token F1 Score.
  - Phân tích chất lượng dữ liệu đầu vào (Quality Checks) và độ tươi mới của dữ liệu (Freshness Report).
- **Garbage In -> Garbage Out Simulation**: Cố tình làm hỏng dữ liệu (Corruption Flow) và sửa chữa lại (Repair Flow) để quan sát sự suy giảm/phục hồi của các chỉ số, chứng minh tầm quan trọng của Data Cleanliness.
- **Visual Dashboard**: Trực quan hóa toàn bộ quá trình bằng một giao diện **Streamlit** chuyên nghiệp.

---

## 🏗️ 2. Phương pháp thực hiện & Kiến trúc (Methodology)

Hệ thống được thiết kế theo cấu trúc Module hóa rõ ràng:

- **`src/ingestion/`**: Chứa logic gọi Crossref API (`crossref.py`), làm sạch dữ liệu (`cleaning.py`), và mô phỏng lỗi dữ liệu (`corruption.py`).
- **`src/retrieval/`**: 
  - `embeddings.py`: Xử lý Embedding với mô hình MiniLM.
  - `index.py`: Quản lý Vector Store cục bộ với ChromaDB.
  - `llm.py` & `qa.py`: Cấu hình LLM Client (Qwen) và logic truy vấn RAG.
  - `agent.py`: LangChain Agent để điều phối quá trình suy luận.
- **`src/evaluation/`**: 
  - `testset.py`: Dùng LLM sinh ra câu hỏi/đáp án tham chiếu từ Cleaned Data.
  - `metrics.py`: Trực tiếp chấm điểm câu trả lời của Agent so với tham chiếu.
- **`src/observability/`**:
  - `quality.py`: Quét Data Quality (tỉ lệ missing, text length, schema validation).
  - `reporting.py`: Tổng hợp báo cáo Markdown cho từng Phase.
- **`src/pipelines/`**:
  - `phase1.py`: Baseline Pipeline (Ingest -> Clean -> Embed -> Eval).
  - `corruption_flow.py`: Corruption & Repair Pipeline để theo dõi metrics.
- **`src/app.py`**: **Streamlit WebUI** bao gồm 3 tính năng:
  - **Observability Metrics**: So sánh biểu đồ RAG Metrics giữa 3 trạng thái (Baseline, Corrupted, Repaired).
  - **Execution Visualization**: Mô phỏng animation cho Pipeline Flow.
  - **Runtime Agent Trace**: Cửa sổ Chat tương tác trực tiếp với Agent, kèm khả năng "Trace" (mổ xẻ) đoạn mã Context được Retrival từ ChromaDB.

---

## 📈 3. Kết quả đạt được (Results)

Dự án đã triển khai thành công 100% các Phase theo PRD:
1. **Pipeline Hoạt Động Ổn Định**: Tự động kéo dữ liệu thật (Crossref), làm sạch, nhúng vector, và lưu vào ChromaDB cục bộ.
2. **LLM-as-a-judge Hoàn Thiện**: Điểm số (Context Precision, Recall, F1) được chấm tự động bằng Qwen LLM API một cách khách quan thay vì rule-based.
3. **Minh chứng rõ ràng cho "Garbage In -> Garbage Out"**: Hệ thống ghi nhận được sự tụt giảm nghiêm trọng của Accuracy và F1 Score khi dữ liệu bị "Corrupt" (vd: thiếu abstract, text rác), và phục hồi lại khi chạy "Repair".
4. **Streamlit UI/UX Tuyệt Vời**:
   - Biểu đồ Plotly động trực quan hóa chất lượng mô hình.
   - Flow Animation theo sát tiến trình Pipeline theo thời gian thực (Runtime tracing).
   - Tương tác QA Agent siêu tốc cùng hiển thị "bằng chứng" (Context) truy xuất rõ ràng.
5. **Robust Testing**: Hệ thống UI được tự động hóa testing với `AppTest` (Streamlit Testing Framework) giả lập toàn bộ hành vi user (Click, Input, Fallback) mượt mà.

---

## 🚀 4. Hướng dẫn cài đặt & Chạy (How to Run)

### Bước 1: Chuẩn bị môi trường & Cài đặt
Dự án sử dụng Python `3.12` và quản lý package (khuyến nghị dùng `uv` hoặc `pip`):
```bash
# Tạo và kích hoạt môi trường ảo
python3 -m venv .venv
source .venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt
```

### Bước 2: Cấu hình biến môi trường
Tạo file `.env` ở thư mục gốc (hoặc copy từ `.env.example`) và điền API Key cho Qwen LLM (OpenAI Compatible):
```ini
LLM_API_KEY=sk-your-qwen-api-key-here
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1/
```

### Bước 3: Khởi chạy Data Pipeline (Tạo Data & Vector Index)
Bạn cần chạy 2 file pipeline để hệ thống tự động tải data, build ChromaDB Index và chạy Evaluation (Sinh báo cáo Metrics):
```bash
# Chạy Baseline Pipeline (Phase 1)
PYTHONPATH=src python src/pipelines/phase1.py

# Chạy Corrupted & Repaired Pipeline (Phase 5)
PYTHONPATH=src python src/pipelines/corruption_flow.py
```
*(Quá trình này mất khoảng vài phút tùy tốc độ API LLM để thực hiện Evaluate).*

### Bước 4: Khởi chạy Giao diện Streamlit Dashboard
Sau khi Pipeline báo SUCCESS và sinh ra dữ liệu trong mục `data/`, bạn khởi chạy WebUI:
```bash
PYTHONPATH=src streamlit run src/app.py
```
👉 Truy cập đường dẫn `http://localhost:8501` trên trình duyệt để tương tác với Agent và xem Dashboard.

### Bước 5: Chạy Auto-Test
Để kiểm tra lại toàn bộ logic hệ thống (bao gồm UI testing):
```bash
PYTHONPATH=src pytest tests/ -s -v
```

---
*Dự án hoàn thành Phase 6 với đầy đủ tính năng. Source code đã được refactor chuẩn Clean Code, thư mục gọn gàng, metrics lưu trữ minh bạch tại `data/`.*
