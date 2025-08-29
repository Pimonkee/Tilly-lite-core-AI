"""
Compatibility shim for legacy imports.
Deprecated: Import from 'tilly_l_l_m_provider_manager' instead of 'tilly_l_l_m_provider'.
This preserves legacy imports while consolidating the implementation.
"""
import warnings as _warnings

_warnings.warn(
    "tilly_l_l_m_provider is deprecated; use tilly_l_l_m_provider_manager instead",
    DeprecationWarning,
    stacklevel=2,
)

from tilly_l_l_m_provider_manager import *  # noqa: F401,F403

