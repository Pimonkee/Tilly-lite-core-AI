"""
Compatibility shim for legacy imports.
Deprecated: Import from 'tilly.config' directly instead of 'tilly_configuration_manager'.
"""
import warnings as _warnings

_warnings.warn(
    "tilly_configuration_manager is deprecated; import from tilly.config",
    DeprecationWarning,
    stacklevel=2,
)

from tilly.config import *  # noqa: F401,F403
