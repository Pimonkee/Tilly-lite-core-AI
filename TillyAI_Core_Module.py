"""
Tilly - The Revolutionary AI Companion
Built with ethics, empathy, and just the right amount of chaos.
"""

__version__ = "1.0.0"
__author__ = "Tilly Development Team"

from .core.types import TillyContext, IntentType, MoodState, StyleVector
from .app.pipeline import TillyPipeline
from .io.config import TillyConfigManager

# Easy imports for quick usage
__all__ = [
    'TillyContext',
    'IntentType', 
    'MoodState',
    'StyleVector',
    'TillyPipeline',
    'TillyConfigManager'
]
