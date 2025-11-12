"""
Tilly Core Types - The DNA of Intelligence
Every conversation flows through these structures.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Protocol, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import uuid

class IntentType(Enum):
    """User's underlying intent"""
    WELLNESS = "wellness"      # Needs therapeutic support
    CRISIS = "crisis"          # In immediate danger
    CHAT = "chat"             # Casual conversation
    UNKNOWN = "unknown"       # Unclear intent

class MoodState(Enum):
    """Emotional state detection"""
    VULNERABLE = "vulnerable"  # Needs extra care
    POSITIVE = "positive"      # Happy, excited
    NEUTRAL = "neutral"        # Balanced state
    AGITATED = "agitated"      # Frustrated, angry

class StyleVector(Enum):
    """Communication style preferences"""
    PLAYFUL = "playful"        # Emojis, excitement
    FORMAL = "formal"          # Professional tone
    CASUAL = "casual"          # Relaxed, friendly
    EMPATHETIC = "empathetic"  # Deep validation

@dataclass
class TillyMemorySnapshot:
    """A moment in conversation time"""
    timestamp: float
    user_text: str
    tilly_response: str
    context: Dict[str, Any]
    session_id: str

@dataclass 
class TillyContext:
    """
    The beating heart of every conversation.
    Carries emotional intelligence through the entire pipeline.
    """
    # Core classification
    intent: IntentType = IntentType.UNKNOWN
    mood: MoodState = MoodState.NEUTRAL
    style_vector: StyleVector = StyleVector.CASUAL
    
    # Safety & ethics scores
    crisis_level: float = 0.0          # 0.0-1.0, higher = more urgent
    ethics_score: float = 1.0          # 1.0 = perfectly ethical
    vulnerability_index: float = 0.0   # 0.0-1.0, higher = needs more care
    
    # Conversation metadata
    user_text: str = ""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    turn_number: int = 0
    
    # Pipeline state
    processing_stage: str = "start"
    model_used: str = ""
    response_candidates: List[str] = field(default_factory=list)
    
    # Extensible metadata for modules
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def update_stage(self, stage: str) -> TillyContext:
        """Update processing stage for debugging"""
        self.processing_stage = stage
        return self
        
    def is_crisis(self) -> bool:
        """Quick crisis check"""
        return self.intent == IntentType.CRISIS or self.crisis_level > 0.8
        
    def needs_gentle_care(self) -> bool:
        """Check if user needs extra empathetic treatment"""
        return (self.mood == MoodState.VULNERABLE or 
                self.vulnerability_index > 0.7 or
                self.is_crisis())

# Type hints for pipeline modules
TillyProcessor = Callable[[str, TillyContext], tuple[str, TillyContext]]
AsyncTillyProcessor = Callable[[str, TillyContext], tuple[str, TillyContext]]

class TillyModule(Protocol):
    """Protocol that all pipeline modules must implement"""
    
    name: str
    
    async def process(self, text: str, context: TillyContext) -> tuple[str, TillyContext]:
        """Process text and context, return updated versions"""
        ...
    
    def validate_input(self, text: str, context: TillyContext) -> bool:
        """Validate that inputs are safe to process"""
        ...
