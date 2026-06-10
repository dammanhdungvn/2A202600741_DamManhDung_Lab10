import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from core.config import load_settings
from core.utils import read_json
from retrieval.index import LocalEmbeddingIndex
from retrieval.qa import answer_question

st.set_page_config(page_title="AI Data Observability Dashboard", layout="wide", page_icon="🕵️")

@st.cache_resource
def get_settings():
    return load_settings()

settings = get_settings()

st.title("🕵️ Data Observability & AI Trace Dashboard")
st.markdown("""
Dashboard này minh họa bài toán **"Garbage In → Garbage Out"** và các kỹ thuật **Data Observability** trong Lab 10.
""")

tab1, tab2, tab3 = st.tabs([
    "📊 1. Observability Metrics (Data Quality)", 
    "🔄 2. Pipeline Execution Flow", 
    "🤖 3. Runtime Agent Trace"
])

# --- TAB 1: Observability Metrics ---
with tab1:
    st.header("So sánh chất lượng RAG qua các giai đoạn (Garbage In -> Garbage Out)")
    
    # Load metrics
    try:
        baseline = read_json(settings.paths.baseline_metrics)
        corrupted = read_json(settings.paths.corrupted_metrics)
        repaired = read_json(settings.paths.repaired_metrics)
        
        # Build dataframe
        df_metrics = pd.DataFrame([
            {"Stage": "1. Baseline (Sạch)", "Judge Accuracy": baseline["judge_accuracy"], "Token F1": baseline["mean_token_f1"]},
            {"Stage": "2. Corrupted (Bẩn)", "Judge Accuracy": corrupted["judge_accuracy"], "Token F1": corrupted["mean_token_f1"]},
            {"Stage": "3. Repaired (Phục hồi)", "Judge Accuracy": repaired["judge_accuracy"], "Token F1": repaired["mean_token_f1"]},
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🤖 Qwen LLM-as-a-judge Accuracy")
            fig = px.bar(df_metrics, x="Stage", y="Judge Accuracy", text="Judge Accuracy", 
                         color="Stage", color_discrete_sequence=["#2E86C1", "#E74C3C", "#27AE60"])
            fig.update_traces(texttemplate='%{text:.1%}', textposition='outside')
            fig.update_layout(yaxis_tickformat='.0%', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("📝 Mean Token F1 Score")
            fig2 = px.line(df_metrics, x="Stage", y="Token F1", markers=True, text="Token F1")
            fig2.update_traces(texttemplate='%{text:.3f}', textposition='top center', 
                               line=dict(color="#8E44AD", width=4), marker=dict(size=12))
            fig2.update_layout(yaxis_range=[0, 1])
            st.plotly_chart(fig2, use_container_width=True)
            
        st.info("💡 **Phân tích:** Khi Data bị bẩn (mất Summary, sai Date), chất lượng câu trả lời của RAG tụt giảm nghiêm trọng. Quality Gates đã phát hiện lỗi này, từ đó kích hoạt luồng Repair để phục hồi lại hiệu suất.")
    except Exception as e:
        st.warning(f"Chưa có đủ data report để vẽ biểu đồ. Hãy chạy Pipeline trước. Error: {e}")

# --- TAB 2: Pipeline Execution Flow ---
with tab2:
    st.header("Mô phỏng Execution Visualization")
    st.markdown("Tiến trình dữ liệu đi từ Source đến Agent Vector Store.")
    
    if st.button("▶️ Chạy mô phỏng Data Pipeline"):
        with st.status("Đang chạy luồng Ingestion & Quality Gates...", expanded=True) as status:
            st.write("📥 1. Đang tải Raw Records từ API...")
            time.sleep(1)
            st.write("🧹 2. Đang Clean Data & Chuẩn hóa Text...")
            time.sleep(1)
            st.write("🚧 3. Chạy Quality Gates (Schema, Freshness, Dedup)...")
            time.sleep(1.5)
            st.write("✔️ Quality Gates Passed!")
            time.sleep(0.5)
            st.write("🧠 4. Đang tạo Chunk & Embeddings (all-MiniLM-L6-v2)...")
            time.sleep(1.5)
            st.write("🗄️ 5. Upsert vào ChromaDB...")
            time.sleep(1)
            status.update(label="Pipeline hoàn tất thành công!", state="complete", expanded=False)
        st.success("Dữ liệu đã sẵn sàng cho Retrieval!")

# --- TAB 3: Runtime Agent Trace ---
with tab3:
    st.header("Tương tác & Theo dõi Agent (Runtime Trace)")
    st.markdown("Hãy hỏi thử một câu. Giao diện sẽ trace lại từng bước truy xuất dữ liệu.")
    
    @st.cache_resource
    def get_index():
        try:
            if settings.paths.repaired_embeddings_json.exists():
                return LocalEmbeddingIndex.load(settings, settings.paths.repaired_embeddings_json)
            elif settings.paths.embeddings_json.exists():
                return LocalEmbeddingIndex.load(settings, settings.paths.embeddings_json)
            return None
        except Exception as e:
            return None
            
    index = get_index()
    
    if index is None:
        st.error("Chưa tìm thấy ChromaDB Index hoặc Data. Hãy chạy pipeline trước.")
    else:
        question = st.text_input("Nhập câu hỏi liên quan đến AI/LLM/RAG (ví dụ: What is agentic AI?):")
        
        if st.button("Gửi / Trace"):
            if not question:
                st.warning("Vui lòng nhập câu hỏi.")
            else:
                with st.spinner("Agent đang suy nghĩ và lục tìm tài liệu..."):
                    result = answer_question(question, settings, index, top_k=4)
                    
                    st.markdown("### 💬 Trả lời của Agent:")
                    st.info(result.answer)
                    
                    st.markdown("### 🔍 Trace Visibility (Lớp Retrieval)")
                    with st.expander("Bấm để xem Agent đã đọc những tài liệu nào (Hit chunks)"):
                        st.write(f"**Số lượng tài liệu Agent lấy lên làm context:** {len(result.retrieved_titles)}")
                        for idx, (title, ctx, doc_id) in enumerate(zip(result.retrieved_titles, result.retrieved_contexts, result.retrieved_doc_ids)):
                            st.markdown(f"**{idx+1}. {title}** *(ID: {doc_id})*")
                            st.caption(f"Context: {ctx[:300]}...")
