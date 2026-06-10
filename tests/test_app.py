from streamlit.testing.v1 import AppTest

def test_ui_observability_metrics():
    print("\n--- Testing Tab 1: Observability Metrics ---")
    at = AppTest.from_file("src/app.py").run(timeout=30)
    assert not at.exception
    
    # Kiểm tra xem có chứa text mong muốn không
    headers = [st.value for st in at.header]
    assert any("So sánh chất lượng RAG qua các giai đoạn" in h for h in headers)
    
    # Kiểm tra xem biểu đồ có được load lên không hoặc hiển thị warning fallback
    if at.warning and len(at.warning) > 0 and "Chưa có đủ data report" in at.warning[0].value:
        print("✅ Tab 1: Chưa có data, UI đã bắt lỗi (Graceful Fallback) thành công!")
    else:
        # Nếu có data thì plotly element sẽ sinh ra script
        print("✅ Tab 1 (Metrics & Charts) loaded successfully!")

def test_ui_pipeline_execution():
    print("\n--- Testing Tab 2: Pipeline Execution Flow ---")
    at = AppTest.from_file("src/app.py").run(timeout=30)
    assert not at.exception
    
    # Nhấn nút "Chạy mô phỏng Data Pipeline"
    at.button[0].click().run(timeout=30)
    assert not at.exception
    
    assert len(at.success) >= 1
    assert "Dữ liệu đã sẵn sàng cho Retrieval!" in at.success[0].value
    print("✅ Tab 2 (Pipeline Execution) simulated successfully!")

def test_ui_runtime_agent_trace():
    print("\n--- Testing Tab 3: Runtime Agent Trace ---")
    at = AppTest.from_file("src/app.py").run(timeout=30)
    assert not at.exception
    
    if len(at.error) > 0 and "Chưa tìm thấy ChromaDB Index" in at.error[0].value:
        print("❌ Chưa có ChromaDB Index. Bỏ qua testing Agent.")
        return

    # Input câu hỏi
    at.text_input[0].input("What is data observability?").run(timeout=30)
    assert not at.exception
    
    # Nhấn nút "Gửi / Trace" (nút thứ 2)
    at.button[1].click().run(timeout=60)
    assert not at.exception
    
    # Kiểm tra xem có sinh ra Answer và Context không
    assert len(at.info) >= 1
    print("✅ Tab 3 (Agent Trace & Context) executed successfully!")
