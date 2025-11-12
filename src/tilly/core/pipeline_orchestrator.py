"""
Pipeline Orchestrator

This module provides a minimal orchestrator placeholder for Tilly's conversation pipeline.
It is intentionally lightweight to avoid import-time errors while the full package
structure evolves. Replace with a full implementation when the package layout is ready.
"""
from __future__ import annotations
from typing import Any, Dict

class PipelineOrchestrator:
    def __init__(self):
        self.state: Dict[str, Any] = {"status": "idle"}

    def run_once(self, user_text: str) -> Dict[str, Any]:
        # Minimal placeholder logic
        return {
            "input": user_text,
            "output": "This is a placeholder response from the orchestrator.",
            "status": "ok",
        }

# Simple functional alias
_orchestrator: PipelineOrchestrator | None = None

def get_orchestrator() -> PipelineOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = PipelineOrchestrator()
    return _orchestrator
