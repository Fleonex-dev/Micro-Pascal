from typing import Dict, Any
import json
import os

class DocumentPerception:
    """
    Interface for the 'Eyes' of the system. 
    In prod, this wraps a Vision Transformer (like UniTable).
    Here, we mock the result to focus on the agentic logic.
    """
    def analyze_document(self, doc_path: str) -> Dict[str, Any]:
        print(f"👁️ [Perception]: Scanning {doc_path} with Vision Model...")
        
        # MOCK: Pretend we parsed a complex table perfectly
        # In a real scenario, we might read the json file, but here we can just return hardcoded data 
        # or read the mock file we just created if we want to be fancy.
        # Let's read the mock file to be slightly more realistic about data locations.
        
        mock_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mocks", "10k_data.json")
        try:
            with open(mock_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback if file not found (though it should be there)
            return {
                "tables": {"data": {"2024": "$5.5B"}},
                "text_chunks": []
            }
