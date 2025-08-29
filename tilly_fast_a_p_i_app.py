"""
Compatibility wrapper for historical imports.
This module re-exports the FastAPI app and models from main.py.
Deprecated: Prefer importing from 'main' directly.
"""
import warnings as _warnings

_warnings.warn(
    "tilly_fast_a_p_i_app is deprecated; import app and models from main",
    DeprecationWarning,
    stacklevel=2,
)

from main import app, ChatRequest, ChatResponse, HealthResponse  # noqa: F401

# Optional: allow running directly for convenience
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
