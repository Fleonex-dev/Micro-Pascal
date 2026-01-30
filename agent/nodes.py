from agent.state import AnalystState
from core.knowledge import build_mock_financial_graph
from core.perception import DocumentPerception
from typing import Dict, Any

import logging

logger = logging.getLogger(__name__)

# Initialize tools
# In a real app, these might be injected or initialized in a more robust way
kg = build_mock_financial_graph()
perception = DocumentPerception()

def planner_node(state: AnalystState) -> Dict[str, Any]:
    """Decomposes the query into steps."""
    logger.info("🧠 [Planner]: Analyzing query...")
    # Mocking LLM planning logic
    plan = [
        "1. Identify ownership structure of ShellCompany_X",
        "2. Retrieve 2024 revenue data",
        "3. Cross-reference ownership with revenue",
        "4. Synthesize final report"
    ]
    return {"plan": plan, "audit_log": [f"Plan created: {plan}"]}

def retrieval_node(state: AnalystState) -> Dict[str, Any]:
    """Executes the plan using tools."""
    logger.info("🕵️: Gathering evidence...")
    evidence = []
    
    # 1. Query Graph
    graph_data = kg.query_relationships("ShellCompany_X")
    evidence.extend(graph_data)
    
    # 2. Query Perception (Table data)
    # We assume the file is somehow known or passed in context. 
    # For this demo, we hardcode the file reference as per the readme example logic.
    doc_data = perception.analyze_document("fake_10k.pdf")
    # Safe retrieval in case keys are missing in mock
    rev_2024 = doc_data.get('tables', {}).get('data', {}).get('2024', "Unknown")
    evidence.append(f"2024 Revenue was {rev_2024}")
    
    return {"evidence": evidence, "audit_log": [f"Evidence gathered: {len(evidence)} items"]}

def reasoning_node(state: AnalystState) -> Dict[str, Any]:
    """Synthesizes the answer."""
    logger.info("📝: Drafting response...")
    evidence_text = "\n".join(state.get('evidence', []))
    # Mock LLM Synthesis
    # In a real app, we would call an LLM here with the evidence
    answer = f"Based on the analysis: Mr. Smith controls ShellCompany_X (via HoldingCompany_Y). The company revenue is $5.5B."
    return {"answer": answer}

def audit_node(state: AnalystState) -> Dict[str, Any]:
    """The 'Safety' layer. Checks for hallucinations."""
    logger.info("🛡️ [Audit]: Verifying citations...")
    
    # Simple check: Does the answer contain numbers found in evidence?
    # Mock logic: We'll just assume it passes for the happy path
    verified = True 
    
    if verified:
        return {"audit_log": ["Audit passed: Verification successful"]}
    else:
        # Loop back logic would go here, effectively incrementing revision_count
        return {"revision_count": state['revision_count'] + 1, "audit_log": ["Audit failed: Revision requested"]}
