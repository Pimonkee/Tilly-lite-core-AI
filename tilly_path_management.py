"""
Compatibility shim for legacy imports.
Deprecated: Import from 'tilly.path_management' instead of 'tilly_path_management'.
"""
import warnings as _warnings

_warnings.warn(
    "tilly_path_management is deprecated; use tilly.path_management",
    DeprecationWarning,
    stacklevel=2,
)

from tilly.path_management import *  # noqa: F401,F403
