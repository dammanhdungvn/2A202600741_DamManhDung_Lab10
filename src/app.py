import streamlit as st
import pandas as pd
import plotly.express as px
from core.config import load_settings
from core.utils import read_json
from retrieval.index import LocalEmbeddingIndex
from retrieval.qa import answer_question

st.set_page_config(page_title="AI Data Observability", layout="wide", page_icon="🕵️")

@st.cache_resource
def get_settings():
    return load_settings()

settings = get_settings()

st.title("🕵️ RAG Data Observability & AI Trace")

tab_guide, tab_data, tab_practice = st.tabs(["📚 Hướng dẫn & Tóm tắt", "📊 Khám phá Dữ liệu", "🛠️ Thực hành AI Observability"])

# --- TAB INTRO ---
with tab_guide:
    st.header("1. Bài toán: Garbage In -> Garbage Out")
    st.markdown("""
    Hệ thống AI/RAG dù có dùng model LLM "xịn" đến đâu, nếu dữ liệu nạp vào là "rác" thì câu trả lời xuất ra cũng sẽ là "rác". 
    **Data Observability (Khả năng quan sát dữ liệu)** ra đời để giải quyết vấn đề này. Nó giống như một "trạm kiểm dịch", chặn đứng dữ liệu xấu trước khi chúng lọt vào bộ não của AI.
    """)

    st.header("2. Flow Thực hiện (Pipeline)")
    st.markdown("""
    Để chứng minh tầm quan trọng của dữ liệu, hệ thống tự động thực thi luồng ETL sau:
    - 📥 **Ingestion:** Kéo tự động hàng ngàn bài báo khoa học mới nhất từ Crossref API.
    - 🧹 **Cleaning:** Đảm bảo chữ thuần túy (clean text), loại bỏ nhiễu HTML giúp AI đọc hiểu dễ dàng hơn.
    - 🚧 **Quality Gates:** Chặn đứng 'Garbage In'. Nếu bài báo thiếu nội dung hoặc quá cũ, nó sẽ bị loại bỏ ngay lập tức.
    - 🧠 **Embedding:** Dịch văn bản thành dãy số (Vector) bằng `all-MiniLM-L6-v2`.
    - 🗄️ **Storage:** Nạp vào ChromaDB - 'não bộ' tốc độ cao cho Agent.
    """)
    
    st.header("3. Làm sao để đo lường và có được Dữ liệu vẽ Biểu đồ?")
    st.markdown("""
    > 👉 Bằng cách này, chúng ta có được dữ liệu thực tế minh bạch để chứng minh: **AI chỉ trả lời chính xác khi dữ liệu đầu vào Sạch!** 
    
    *Chuyển sang Tab 2 để tự tay thay đổi Database và xem AI thay đổi thái độ ra sao!*
    """)

# --- TAB DATA EXPLORER ---
with tab_data:
    st.header("🔍 Trực quan hóa Dữ liệu (Data Explorer)")
    st.markdown("Quan sát trực tiếp dữ liệu ở 3 giai đoạn để hiểu rõ quá trình làm sạch và phục hồi ảnh hưởng thế nào đến chất lượng.")
    
    tab_base, tab_corr, tab_rep = st.tabs(["🟢 1. Baseline (Sạch)", "🔴 2. Corrupted (Raw/Bẩn)", "🟡 3. Repaired (Phục hồi)"])
    
    with tab_base:
        try:
            data = read_json(settings.paths.embeddings_json)["documents"]
            df_view = pd.DataFrame(data)[["paper_id", "title", "content"]]
            st.caption("✨ Dữ liệu đã qua Pipeline làm sạch (Bỏ thẻ HTML, chuẩn hóa text, loại bỏ Null). Chỉ hiển thị 10 dòng đầu để tránh quá tải.")
            st.dataframe(df_view.head(10), use_container_width=True)
        except Exception as e:
            st.warning(f"⚠️ Lỗi hiển thị dữ liệu Baseline: {e}")

    with tab_corr:
        try:
            data = read_json(settings.paths.corrupted_embeddings_json)["documents"]
            df_view = pd.DataFrame(data)[["paper_id", "title", "content"]]
            st.caption("🗑️ Dữ liệu thô (Raw) lấy thẳng từ API, chứa các thẻ HTML, danh sách lộn xộn và thiếu chuẩn hóa. Hiển thị 10 dòng đầu.")
            st.dataframe(df_view.head(10), use_container_width=True)
        except Exception as e:
            st.warning(f"⚠️ Lỗi hiển thị dữ liệu Corrupted: {e}")

    with tab_rep:
        try:
            data = read_json(settings.paths.repaired_embeddings_json)["documents"]
            df_view = pd.DataFrame(data)[["paper_id", "title", "content"]]
            st.caption("🔧 Dữ liệu đã được Phục hồi qua hệ thống Data Quality Gates. Hiển thị 10 dòng đầu.")
            st.dataframe(df_view.head(10), use_container_width=True)
        except Exception as e:
            st.warning(f"⚠️ Lỗi hiển thị dữ liệu Repaired: {e}")

# --- TAB INTERACTIVE ---
with tab_practice:
    st.header("Tương tác & Theo dõi Agent (Runtime Trace)")
    st.markdown("Hãy chọn loại Database, xem Chart thay đổi, và chat với Agent để thấy sự khác biệt!")
    
    # 1. Chọn Database
    data_choice = st.radio("Cấu hình Database (Thử nghiệm Garbage In -> Garbage Out):", 
                           ["🟢 Sạch (Baseline)", "🔴 Bẩn (Corrupted)", "🟡 Phục hồi (Repaired)"], 
                           horizontal=True)
                           
    if "Sạch" in data_choice:
        selected_stage = "1. Baseline (Sạch)"
        color_theme = "#27AE60"
    elif "Bẩn" in data_choice:
        selected_stage = "2. Corrupted (Bẩn)"
        color_theme = "#E74C3C"
    else:
        selected_stage = "3. Repaired (Phục hồi)"
        color_theme = "#F1C40F"
        
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    st.markdown("---")
    col_chart, col_chat = st.columns([1.1, 1])
    
    with col_chart:
        st.subheader("📊 Chất lượng Hệ thống")
        try:
            baseline = read_json(settings.paths.baseline_metrics)
            corrupted = read_json(settings.paths.corrupted_metrics)
            repaired = read_json(settings.paths.repaired_metrics)
            
            # 1. Biểu đồ tĩnh (Kỳ vọng)
            st.markdown(f"**Trạng thái Database hiện tại:** `{selected_stage}`")
            
            df_metrics = pd.DataFrame([
                {"Stage": "1. Baseline (Sạch)", "Judge Accuracy": baseline["judge_accuracy"], "Token F1": baseline["mean_token_f1"]},
                {"Stage": "2. Corrupted (Bẩn)", "Judge Accuracy": corrupted["judge_accuracy"], "Token F1": corrupted["mean_token_f1"]},
                {"Stage": "3. Repaired (Phục hồi)", "Judge Accuracy": repaired["judge_accuracy"], "Token F1": repaired["mean_token_f1"]},
            ])
            
            # --- Lịch sử Realtime ---
            st.markdown("### 📈 Biến động Chất lượng (Real-time History)")
            if len(st.session_state.chat_history) == 0:
                st.info("Hãy đặt câu hỏi ở Chatbot bên cạnh để xem biểu đồ chất lượng Real-time vẽ ở đây!")
                
                # Show the static bar chart as a placeholder
                df_metrics["Color"] = df_metrics["Stage"].apply(lambda x: color_theme if x == selected_stage else "#BDC3C7")
                fig = px.bar(df_metrics, x="Stage", y="Token F1", text="Token F1", color="Stage",
                             color_discrete_sequence=df_metrics["Color"].unique())
                fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
                fig.update_layout(yaxis_tickformat='.2f', showlegend=False, yaxis_range=[0, 1.0], height=300)
                st.plotly_chart(fig, width='stretch')
            else:
                # Vẽ biểu đồ Line chart cho lịch sử
                df_history = pd.DataFrame(st.session_state.chat_history)
                fig_hist = px.line(df_history, x="Lần hỏi", y="F1 Score", markers=True, text="F1 Score",
                                   color="Database", title="Hành trình Test Garbage In -> Garbage Out của bạn")
                fig_hist.update_traces(texttemplate='%{text:.3f}', textposition='top center', 
                                       marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))
                fig_hist.update_layout(yaxis_tickformat='.2f', yaxis_range=[0, 1.0], height=350)
                st.plotly_chart(fig_hist, width='stretch')
                
                # Bảng chi tiết
                st.dataframe(df_history[["Lần hỏi", "Database", "Câu hỏi", "F1 Score"]].tail(5), use_container_width=True)
                
            st.caption("ℹ️ **F1 Score:** Đo lường độ bám sát của câu trả lời với tài liệu gốc. Dữ liệu rác làm AI phải 'đoán mò' (ảo giác), dẫn tới F1 giảm mạnh.")
            
        except Exception as e:
            st.warning("Chưa có đủ data report để vẽ biểu đồ. Hãy chạy Pipeline trước.")
            
    with col_chat:
        st.subheader("🤖 Chatbot (Agent Trace)")
        
        def get_specific_index(choice_str):
            try:
                if "Sạch" in choice_str and settings.paths.embeddings_json.exists():
                    return LocalEmbeddingIndex.load(settings, settings.paths.embeddings_json)
                elif "Bẩn" in choice_str and settings.paths.corrupted_embeddings_json.exists():
                    return LocalEmbeddingIndex.load(settings, settings.paths.corrupted_embeddings_json)
                elif "Phục hồi" in choice_str and settings.paths.repaired_embeddings_json.exists():
                    return LocalEmbeddingIndex.load(settings, settings.paths.repaired_embeddings_json)
                return None
            except Exception as e:
                return None
                
        index = get_specific_index(data_choice)
        
        if index is None:
            st.error("Chưa tìm thấy ChromaDB Index hoặc Data. Hãy chạy pipeline trước.")
        else:
            st.markdown("**💡 Gợi ý câu hỏi (Click để điền nhanh):**")
            
            def set_question(q):
                st.session_state.user_question = q
                
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            col_btn1.button("Data Observability là gì?", on_click=set_question, args=("What is data observability?",))
            col_btn2.button("Làm sao để đánh giá RAG?", on_click=set_question, args=("How to evaluate RAG pipelines?",))
            col_btn3.button("Tại sao phải làm sạch data?", on_click=set_question, args=("Why is data cleaning important for LLMs?",))
            
            # Text input linked to session_state key
            question = st.text_input("Nhập câu hỏi của bạn:", key="user_question")
            
            if st.button("Gửi / Trace", key="submit_trace"):
                if not question:
                    st.warning("Vui lòng nhập câu hỏi.")
                else:
                    with st.spinner(f"Agent đang tìm tài liệu trong Database {selected_stage}..."):
                        result = answer_question(question, settings, index, top_k=4)
                        
                        # Lưu lịch sử
                        stage_dict = {
                            "1. Baseline (Sạch)": baseline,
                            "2. Corrupted (Bẩn)": corrupted,
                            "3. Repaired (Phục hồi)": repaired
                        }
                        current_acc = stage_dict[selected_stage]["judge_accuracy"]
                        current_f1 = stage_dict[selected_stage]["mean_token_f1"]
                        
                        st.session_state.chat_history.append({
                            "Lần hỏi": f"Lần {len(st.session_state.chat_history) + 1}",
                            "Database": selected_stage,
                            "Câu hỏi": question,
                            "Accuracy (Chất lượng)": current_acc,
                            "F1 Score": current_f1
                        })
                        
                        st.markdown("### 💬 Trả lời của Agent:")
                        st.info(result.answer)
                        
                        st.markdown("### 🔍 Trace Visibility")
                        with st.expander("Bấm để xem tài liệu Gốc (Hit chunks)"):
                            st.write(f"**Số lượng tài liệu Agent lấy lên:** {len(result.retrieved_titles)}")
                            for idx, (title, ctx, doc_id) in enumerate(zip(result.retrieved_titles, result.retrieved_contexts, result.retrieved_doc_ids)):
                                st.markdown(f"**{idx+1}. {title}** *(ID: {doc_id})*")
                                st.caption(f"Context: {ctx[:300]}...")
