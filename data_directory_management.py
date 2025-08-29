"""
Compatibility shim: re-export directory/path helpers from tilly_path_management.
"""
from tilly_path_management import (
    ensure_data_dirs,
    get_config_path,
    get_model_path,
    get_memory_path,
    get_log_path,
    PROJECT_ROOT,
    DATA_ROOT,
    CONFIG_ROOT,
    MODELS_ROOT,
    MEMORY_ROOT,
    LOGS_ROOT,
)  # noqa: F401
