from core.infrastructure import SiloManager
from agent.graph import app
import logging
import sys

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    silo = SiloManager()
    
    # Simulate a request coming into a specific Tenant Silo
    with silo.execution_context("hedge_fund_a"):
        query = "Who owns ShellCompany_X and what is the revenue?"
        
        logger.info(f"🚀 Starting Analysis for: {query}")
        
        initial_state = {
            "query": query, 
            "revision_count": 0, 
            "audit_log": []
        }
        
        # Run the LangGraph
        result = app.invoke(initial_state)
        
        logger.info("✅ Final Result: %s", result["answer"])
        
        print("\n📜 Compliance Audit Log:")
        for entry in result["audit_log"]:
            print(f" - {entry}")

if __name__ == "__main__":
    main()
