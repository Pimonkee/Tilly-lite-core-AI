"""
Compatibility shim for legacy imports.
Deprecated: Import types from 'tilly_conversation_context' instead of 'tilly_conversation_pipeline'.
"""
import warnings as _warnings

_warnings.warn(
    "tilly_conversation_pipeline is deprecated; import types from tilly_conversation_context",
    DeprecationWarning,
    stacklevel=2,
)

from tilly_conversation_context import *  # noqa: F401,F403
