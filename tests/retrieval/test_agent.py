from unittest.mock import MagicMock
from retrieval.agent import run_agent_question

def test_run_agent_question():
    agent_mock = MagicMock()
    
    class MockMessage:
        def __init__(self, content):
            self.content = content
            
    agent_mock.invoke.return_value = {"messages": [MockMessage("Mocked answer")]}
    
    answer = run_agent_question(agent_mock, "What is AI?")
    assert answer == "Mocked answer"
