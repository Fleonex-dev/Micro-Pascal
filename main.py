from core.infrastructure import SiloManager
from agent.graph import app

def main():
    silo = SiloManager()
    
    # Simulate a request coming into a specific Tenant Silo
    with silo.execution_context("hedge_fund_a"):
        query = "Who owns ShellCompany_X and what is the revenue?"
        
        print(f"\n🚀 Starting Analysis for: {query}\n" + "="*50)
        
        initial_state = {
            "query": query, 
            "revision_count": 0, 
            "audit_log": []
        }
        
        # Run the LangGraph
        result = app.invoke(initial_state)
        
        print("="*50 + "\n✅ Final Result:\n")
        print(result["answer"])
        
        print("\n📜 Compliance Audit Log:")
        for entry in result["audit_log"]:
            print(f" - {entry}")

if __name__ == "__main__":
    main()
