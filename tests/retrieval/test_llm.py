from unittest.mock import MagicMock
from core.config import Settings
from retrieval.llm import build_llm

def test_build_llm_qwen():
    settings = MagicMock(spec=Settings)
    settings.llm_provider = "qwen"
    settings.model_name = "qwen-test"
    settings.qwen_api_key = "test_key"
    settings.qwen_base_url = "test_url"
    
    llm = build_llm(settings)
    assert llm.model_name == "qwen-test"
