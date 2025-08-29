"""
Compatibility shim for legacy imports.
Deprecated: Import from 'tilly_l_l_m_provider_manager' instead of 'tilly_l_l_m_provider_management'.
"""
import warnings as _warnings

_warnings.warn(
    "tilly_l_l_m_provider_management is deprecated; use tilly_l_l_m_provider_manager instead",
    DeprecationWarning,
    stacklevel=2,
)

from tilly_l_l_m_provider_manager import *  # noqa: F401,F403
