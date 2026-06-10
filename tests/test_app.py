from streamlit.testing.v1 import AppTest

def test_app_e2e():
    print("\n--- Testing App E2E (Interactive Tabs) ---")
    at = AppTest.from_file("src/app.py").run(timeout=30)
    assert not at.exception
    
    # Check if Intro Tab content is loaded
    headers = [st.value for st in at.header]
    assert any("Bài toán" in h for h in headers)
    
    if len(at.error) > 0 and "Chưa tìm thấy ChromaDB Index" in at.error[0].value:
        print("❌ Chưa có ChromaDB Index. Bỏ qua testing Agent.")
        return

    # Input question
    at.text_input[0].input("What is data observability?").run(timeout=30)
    assert not at.exception
    
    # Click submit
    at.button(key="submit_trace").click().run(timeout=60)
    assert not at.exception
    
    # Check if answered
    assert len(at.info) >= 1
    print("✅ App Test E2E executed successfully!")
