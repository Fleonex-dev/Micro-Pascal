from langgraph.graph import StateGraph, END
from agent.state import AnalystState
from agent.nodes import planner_node, retrieval_node, reasoning_node, audit_node

# Build the Graph
workflow = StateGraph(AnalystState)
workflow.add_node("planner", planner_node)
workflow.add_node("retriever", retrieval_node)
workflow.add_node("reasoner", reasoning_node)
workflow.add_node("auditor", audit_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "retriever")
workflow.add_edge("retriever", "reasoner")
workflow.add_edge("reasoner", "auditor")
workflow.add_edge("auditor", END)

app = workflow.compile()
