"""
Tilly Path Management
Manages all file paths and directory structures for the application
"""

from src.tilly.config.path_management import (
    DATA_ROOT,
    LOGS_DIR,
    SCREENSHOTS_DIR,
    MEMORY_DIR,
    SESSIONS_DIR,
    CACHE_DIR,
    ensure_data_dirs,
    get_log_path,
    get_screenshot_path,
    get_memory_path,
    get_session_path,
    get_cache_path
)

__all__ = [
    'DATA_ROOT',
    'LOGS_DIR',
    'SCREENSHOTS_DIR',
    'MEMORY_DIR',
    'SESSIONS_DIR',
    'CACHE_DIR',
    'ensure_data_dirs',
    'get_log_path',
    'get_screenshot_path',
    'get_memory_path',
    'get_session_path',
    'get_cache_path'
]

