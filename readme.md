# Micro-Pascal: Autonomous Financial Analyst
**Research Prototype v0.1**

## 🔬 Research Goal

This project serves as a minimal viable architecture (MVA) for an autonomous financial agent capable of performing deep-dive due diligence. The primary research objective is to validate a system architecture that decouples **agentic reasoning** from **data perception** while enforcing strict **tenant isolation** by design.

Core constraints validated in this prototype:
1.  **Strict Multi-Tenancy**: Logical isolation of data at the application layer.
2.  **Structural Knowledge**: Beyond semantic search, utilizing graph traversal for entity relationships.
3.  **Cyclic Reasoning**: Non-linear execution flows for error recovery and audit loops.

---

## 🏗️ System Architecture

The system is composed of four decoupled layers, each addressing a specific engineering challenge in autonomous finance.

### 1. The Isolation Layer ("Silo")
**Component**: `core/infrastructure.py`

**Architectural Decision:**
We implemented a strict `SiloManager` using Python's `contextvars`. This ensures that tenant context (e.g., encryption keys, allowed models) is injected into the execution thread's local storage. This design prevents "context bleeding" where an agent might accidentally access data from another tenant during concurrent execution.

*Implication:* Security policies are enforced at the infrastructure level, not the business logic level.

### 2. The Knowledge Layer (GraphRAG)
**Component**: `core/knowledge.py`

**Architectural Decision:**
Financial entities (Beneficial Owners, Subsidiaries, Holding Companies) form a dense network that vector similarity (RAG) cannot accurately traverse. We implemented a **Directed Knowledge Graph** (backed by NetworkX) to model these deterministic relationships.

*Implication:* Queries like "Who controls company X?" are resolved via graph traversal algorithms (BFS/DFS), yielding 100% precision compared to probabilistic vector retrieval.

### 3. The Perception Interface
**Component**: `core/perception.py`

**Architectural Decision:**
To maintain modularity, the document understanding layer is completely decoupled from the reasoning agent. The `DocumentPerception` detailed interface allows for the underlying implementation (currently a deterministic mock) to be swapped for large-scale Vision Transformers (e.g., UniTable or GPT-4o-Vision) without refactoring the agentic logic.

*Implication:* Accelerates agent development by mocking heavy perception tasks during the logic evaluation phase.

### 4. The Agentic State Machine
**Component**: `agent/graph.py`

**Architectural Decision:**
We utilized **LangGraph** to model the analyst as a state machine rather than a linear chain. This enables:
-   **Cyclic Refinement:** The agent can self-correct if the `Auditor` node detects hallucinations.
-   **State Persistence:** The entire thought process (Plan, Evidence, Audit Log) is serialized, allowing for "Time Travel" debugging and human-in-the-loop verification by compliance officers.

---

## 📂 Repository Structure

```text
micro-pascal/
├── core/
│   ├── infrastructure.py   # SiloManager (Context Isolation)
│   ├── knowledge.py        # KnowledgeEngine (Graph Traversal)
│   └── perception.py       # Perception Interface (Vision Abstraction)
├── agent/
│   ├── graph.py            # State Machine Definition
│   ├── nodes.py            # Functional Logic Nodes
│   └── state.py            # Shared State Schema
├── mocks/                  # Deterministic Test Data
└── main.py                 # Simulation Entry Point
```

## 🚀 Reproduction & Testing

To run the architectural validation simulation:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Execute the simulation
python3 main.py
```

The output will demonstrate the full lifecycle: acquiring a tenant lock, formulating a plan, gathering structural evidence, and passing the compliance audit.