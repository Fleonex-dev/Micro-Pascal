from typing import TypedDict, List, Annotated
import operator

class AnalystState(TypedDict):
    query: str
    plan: List[str]
    evidence: List[str]
    answer: str
    audit_log: Annotated[List[str], operator.add] # Append-only log
    revision_count: int
