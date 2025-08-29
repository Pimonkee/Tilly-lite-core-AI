"""
Compatibility shim for legacy imports.
Deprecated: Import from 'tilly.config' directly instead of 'tilly_configuration_manager3'.
"""
import warnings as _warnings

_warnings.warn(
    "tilly_configuration_manager3 is deprecated; import from tilly.config",
    DeprecationWarning,
    stacklevel=2,
)

from tilly.config import *  # noqa: F401,F403