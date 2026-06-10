import pytest
from src.core.config import Settings, require_llm_credentials

def test_qwen_provider_requires_api_key():
    settings = Settings(
        llm_provider="qwen",
        model_name="qwen3.5-flash",
        google_api_key=None,
        openai_api_key=None,
        anthropic_api_key=None,
        openrouter_api_key=None,
        openrouter_base_url="",
        ollama_base_url="",
        custom_llm_api_key=None,
        custom_llm_base_url=None,
        qwen_api_key=None,  # Missing key
        qwen_base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        baseline_collection_name="b",
        corrupted_collection_name="c",
        repaired_collection_name="r",
        source_api="api",
        source_query="q",
        source_filter="f",
        max_results=10,
        top_k=4,
        freshness_threshold_days=180,
        refresh_source=False,
        refresh_test_set=False,
        paths=None
    )
    with pytest.raises(RuntimeError, match="QWEN_API_KEY is required"):
        require_llm_credentials(settings)

def test_qwen_provider_success():
    settings = Settings(
        llm_provider="qwen",
        model_name="qwen3.5-flash",
        google_api_key=None,
        openai_api_key=None,
        anthropic_api_key=None,
        openrouter_api_key=None,
        openrouter_base_url="",
        ollama_base_url="",
        custom_llm_api_key=None,
        custom_llm_base_url=None,
        qwen_api_key="valid-key",
        qwen_base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        baseline_collection_name="b",
        corrupted_collection_name="c",
        repaired_collection_name="r",
        source_api="api",
        source_query="q",
        source_filter="f",
        max_results=10,
        top_k=4,
        freshness_threshold_days=180,
        refresh_source=False,
        refresh_test_set=False,
        paths=None
    )
    require_llm_credentials(settings) # Should pass
