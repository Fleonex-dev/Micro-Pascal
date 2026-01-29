import networkx as nx
from typing import List, Tuple

class KnowledgeEngine:
    """
    A lightweight GraphRAG implementation using NetworkX.
    Simulates the 'FIBO' ontology relationships.
    """
    def __init__(self):
        self.graph = nx.DiGraph()

    def ingest_fact(self, subject: str, predicate: str, object_: str):
        # In a real system, this would write to Neo4j
        self.graph.add_edge(subject, object_, relation=predicate)

    def query_relationships(self, entity: str, max_depth=2) -> List[str]:
        """
        Performs a traversal to find relationships.
        Solves the 'Ultimate Beneficial Owner' problem.
        """
        if entity not in self.graph:
            return [f"No knowledge found for {entity}"]
        
        results = []
        # Simple BFS traversal to find connected entities
        edges = list(nx.bfs_edges(self.graph, source=entity, depth_limit=max_depth))
        for u, v in edges:
            relation = self.graph[u][v]['relation']
            results.append(f"{u} --[{relation}]--> {v}")
        return results

# Factory to populate mock data
def build_mock_financial_graph():
    kg = KnowledgeEngine()
    # Complex ownership chain (The "Hard" problem for vectors)
    kg.ingest_fact("ShellCompany_X", "owned_by", "HoldingCompany_Y")
    kg.ingest_fact("HoldingCompany_Y", "controlled_by", "Mr_Smith")
    kg.ingest_fact("Mr_Smith", "is_board_member_of", "MegaCorp")
    return kg
