from __future__ import annotations

from dataclasses import dataclass

from core.config import Settings
from retrieval.index import LocalEmbeddingIndex
from retrieval.agent import build_agent, run_agent_question


@dataclass(frozen=True)
class AnswerResult:
    question: str
    answer: str
    retrieved_doc_ids: list[str]
    retrieved_contexts: list[str]
    retrieved_titles: list[str]


def answer_question(question: str, settings: Settings, index: LocalEmbeddingIndex, top_k: int | None = None) -> AnswerResult:
    retrieved = index.search(question, top_k=top_k)
    
    if not retrieved:
        return AnswerResult(
            question=question,
            answer="I don't know from the indexed corpus.",
            retrieved_doc_ids=[],
            retrieved_contexts=[],
            retrieved_titles=[],
        )
        
    agent = build_agent(settings, index)
    answer = run_agent_question(agent, question)
    
    return AnswerResult(
        question=question,
        answer=answer,
        retrieved_doc_ids=[item.paper_id for item in retrieved],
        retrieved_contexts=[item.content for item in retrieved],
        retrieved_titles=[item.title for item in retrieved],
    )
