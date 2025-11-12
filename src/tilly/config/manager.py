"""
Tilly Configuration Manager
Centralizes all configuration and settings management
"""

import os
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """Configuration for an LLM model provider"""
    provider: str  # "gemini", "deepseek", "ollama"
    model_name: str
    api_key: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1024
    endpoint: Optional[str] = None


@dataclass
class TillyConfig:
    """Main Tilly configuration"""
    environment: str = "development"
    primary_model: Optional[ModelConfig] = None
    fallback_model: Optional[ModelConfig] = None
    log_level: str = "INFO"
    data_root: str = "./data"


class TillyConfigManager:
    """Manages Tilly's configuration from environment variables and config files"""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> TillyConfig:
        """Load configuration from environment variables"""
        # Load primary model config
        primary_provider = os.getenv("TILLY_PRIMARY_PROVIDER", "gemini")
        primary_model = ModelConfig(
            provider=primary_provider,
            model_name=os.getenv("TILLY_PRIMARY_MODEL", "gemini-pro"),
            api_key=os.getenv("GEMINI_API_KEY") if primary_provider == "gemini" else os.getenv("DEEPSEEK_API_KEY"),
            temperature=float(os.getenv("TILLY_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("TILLY_MAX_TOKENS", "1024"))
        )
        
        # Load fallback model config if specified
        fallback_provider = os.getenv("TILLY_FALLBACK_PROVIDER")
        fallback_model = None
        if fallback_provider:
            fallback_model = ModelConfig(
                provider=fallback_provider,
                model_name=os.getenv("TILLY_FALLBACK_MODEL", "gemini-pro"),
                api_key=os.getenv("FALLBACK_API_KEY"),
                temperature=0.7,
                max_tokens=1024
            )
        
        config = TillyConfig(
            environment=os.getenv("TILLY_ENV", "development"),
            primary_model=primary_model,
            fallback_model=fallback_model,
            log_level=os.getenv("TILLY_LOG_LEVEL", "INFO"),
            data_root=os.getenv("TILLY_DATA_ROOT", "./data")
        )
        
        logger.info(f"Configuration loaded: {config.environment} environment")
        return config
    
    def get_config(self) -> TillyConfig:
        """Get the current configuration"""
        return self.config


# Singleton instance
_config_manager = None


def get_config() -> TillyConfig:
    """Get the singleton configuration instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = TillyConfigManager()
    return _config_manager.config


def get_config_manager() -> TillyConfigManager:
    """Get the singleton configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = TillyConfigManager()
    return _config_manager
