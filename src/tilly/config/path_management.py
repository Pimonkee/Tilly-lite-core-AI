"""
Tilly Path Management
Manages all file paths and directory structures for the application
"""

from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)

# Base data directory - can be configured via environment
DATA_ROOT = Path(os.getenv("TILLY_DATA_ROOT", "./data"))

# Subdirectories
LOGS_DIR = DATA_ROOT / "logs"
SCREENSHOTS_DIR = DATA_ROOT / "screenshots"
MEMORY_DIR = DATA_ROOT / "memory"
SESSIONS_DIR = DATA_ROOT / "sessions"
CACHE_DIR = DATA_ROOT / "cache"


def ensure_data_dirs():
    """Create all necessary data directories"""
    directories = [
        DATA_ROOT,
        LOGS_DIR,
        SCREENSHOTS_DIR,
        MEMORY_DIR,
        SESSIONS_DIR,
        CACHE_DIR
    ]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")
        except Exception as e:
            logger.error(f"Failed to create directory {directory}: {e}")


def get_log_path(filename: str) -> Path:
    """Get the full path for a log file"""
    ensure_data_dirs()
    return LOGS_DIR / filename


def get_screenshot_path(filename: str) -> Path:
    """Get the full path for a screenshot file"""
    ensure_data_dirs()
    return SCREENSHOTS_DIR / filename


def get_memory_path(filename: str) -> Path:
    """Get the full path for a memory file"""
    ensure_data_dirs()
    return MEMORY_DIR / filename


def get_session_path(session_id: str) -> Path:
    """Get the full path for a session file"""
    ensure_data_dirs()
    return SESSIONS_DIR / f"{session_id}.json"


def get_cache_path(filename: str) -> Path:
    """Get the full path for a cache file"""
    ensure_data_dirs()
    return CACHE_DIR / filename
