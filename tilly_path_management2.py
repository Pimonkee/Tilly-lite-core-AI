"""
Compatibility shim for legacy imports.
Deprecated: Import from 'tilly.path_management' instead of 'tilly_path_management2'.
"""
import warnings as _warnings

_warnings.warn(
    "tilly_path_management2 is deprecated; use tilly.path_management",
    DeprecationWarning,
    stacklevel=2,
)

from tilly_path_management import *  # noqa: F401,F403
