import contextvars
from contextlib import contextmanager
from typing import Optional, List
from dataclasses import dataclass

import logging

logger = logging.getLogger(__name__)

# The "Silo" Context
# This ensures that any DB call or LLM request implicitly knows which tenant it serves.
_current_tenant = contextvars.ContextVar("tenant_id", default=None)

@dataclass
class TenantConfig:
    tenant_id: str
    encryption_key: str  # Mock representation of a KMS key
    allowed_models: List[str]

import os

class SiloManager:
    """
    Simulates the infrastructure control plane. 
    Ensures data isolation between generic 'users'.
    """
    def __init__(self):
        self._configs = {
            "hedge_fund_a": TenantConfig(
                "hedge_fund_a", 
                os.getenv("HF_A_KEY", "key_A_dev"), 
                ["gpt-4o"]
            ),
            "bank_b": TenantConfig(
                "bank_b", 
                os.getenv("BANK_B_KEY", "key_B_dev"), 
                ["claude-3-5"]
            ),
        }

    @contextmanager
    def execution_context(self, tenant_id: str):
        if tenant_id not in self._configs:
            raise ValueError(f"Unauthorized Tenant: {tenant_id}")
        
        token = _current_tenant.set(self._configs[tenant_id])
        try:
            logger.info(f"🔒: Entering Silo for {tenant_id}")
            yield
        finally:
            logger.info(f"🔓: Exiting Silo for {tenant_id}")
            _current_tenant.reset(token)

    @staticmethod
    def get_current_tenant() -> Optional[TenantConfig]:
        return _current_tenant.get()
