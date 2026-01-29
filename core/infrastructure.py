import contextvars
from contextlib import contextmanager
from typing import Optional, List
from dataclasses import dataclass

# The "Silo" Context
# This ensures that any DB call or LLM request implicitly knows which tenant it serves.
_current_tenant = contextvars.ContextVar("tenant_id", default=None)

@dataclass
class TenantConfig:
    tenant_id: str
    encryption_key: str  # Mock representation of a KMS key
    allowed_models: List[str]

class SiloManager:
    """
    Simulates the infrastructure control plane. 
    Ensures data isolation between generic 'users'.
    """
    def __init__(self):
        self._configs = {
            "hedge_fund_a": TenantConfig("hedge_fund_a", "key_A", ["gpt-4o"]),
            "bank_b": TenantConfig("bank_b", "key_B", ["claude-3-5"]),
        }

    @contextmanager
    def execution_context(self, tenant_id: str):
        if tenant_id not in self._configs:
            raise ValueError(f"Unauthorized Tenant: {tenant_id}")
        
        token = _current_tenant.set(self._configs[tenant_id])
        try:
            print(f"🔒: Entering Silo for {tenant_id}")
            yield
        finally:
            print(f"🔓: Exiting Silo for {tenant_id}")
            _current_tenant.reset(token)

    @staticmethod
    def get_current_tenant() -> Optional[TenantConfig]:
        return _current_tenant.get()
