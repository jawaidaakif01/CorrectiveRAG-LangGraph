from typing import List, Optional, TypedDict


class GraphState(TypedDict, total=False):
    """
    Represents the state of our graph

    Attributes:
        question: question
        generation: LLM Generation
        web_search: (boolean) whether to add search
        documents: list of documents
    """

    question: str
    generation: str
    web_search: bool
    documents: List[str]