"""
Tilly Router - The First Guardian
Analyzes incoming text and determines the user's intent with surgical precision.
"""

import re
from typing import Dict, Set
from tilly_conversation_context import TillyContext, IntentType
import logging

logger = logging.getLogger(__name__)

class TillyRouter:
    """
    The Router is Tilly's first line of intelligence - it reads between the lines
    and understands what the human really needs before they even know it themselves.
    """
    
    def __init__(self):
        self.name = "router"
        
        # Crisis indicators - these trigger immediate escalation
        self.crisis_patterns = {
            "suicide": ["suicide", "kill myself", "end my life", "want to die", "better off dead"],
            "self_harm": ["hurt myself", "cut myself", "self harm", "self-harm"],
            "emergency": ["emergency", "help me", "can't go on", "end it all"]
        }
        
        # Wellness indicators - these suggest the user needs therapeutic support
        self.wellness_patterns = {
            "depression": ["depressed", "sad", "hopeless", "empty", "worthless"],
            "anxiety": ["anxious", "panic", "overwhelmed", "worried", "scared"],
            "stress": ["stressed", "pressure", "can't cope", "breaking down"],
            "loneliness": ["lonely", "alone", "isolated", "nobody understands"]
        }
        
        # Positive indicators
        self.positive_patterns = [
            "great", "amazing", "fantastic", "wonderful", "excited", 
            "happy", "thrilled", "excellent", "perfect"
        ]
        
    async def process(self, text: str, context: TillyContext) -> tuple[str, TillyContext]:
        """Process text and determine intent"""
        logger.info(f"Router processing: {text[:50]}...")
        
        text_lower = text.lower()
        
        # First check for crisis - this takes absolute priority
        crisis_score = self._calculate_crisis_score(text_lower)
        if crisis_score > 0.7:
            context.intent = IntentType.CRISIS
            context.crisis_level = crisis_score
            logger.warning(f"CRISIS DETECTED - Score: {crisis_score}")
            return text, context.update_stage("router_crisis")
            
        # Check for wellness needs
        wellness_score = self._calculate_wellness_score(text_lower)
        if wellness_score > 0.5:
            context.intent = IntentType.WELLNESS
            context.vulnerability_index = wellness_score
            logger.info(f"Wellness intent detected - Score: {wellness_score}")
            return text, context.update_stage("router_wellness")
            
        # Default to casual chat
        context.intent = IntentType.CHAT
        logger.info("Chat intent detected")
        return text, context.update_stage("router_chat")
    
    def _calculate_crisis_score(self, text: str) -> float:
        """Calculate how much this text indicates a crisis situation"""
        score = 0.0
        total_indicators = 0
        
        for category, patterns in self.crisis_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    if category == "suicide":
                        score += 1.0  # Maximum urgency
                    elif category == "self_harm":
                        score += 0.8
                    else:
                        score += 0.6
                    total_indicators += 1
        
        # Normalize but cap at 1.0
        return min(1.0, score / max(1, total_indicators)) if total_indicators > 0 else 0.0
    
    def _calculate_wellness_score(self, text: str) -> float:
        """Calculate how much this text indicates wellness needs"""
        score = 0.0
        matches = 0
        
        for category, patterns in self.wellness_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    score += 0.7
                    matches += 1
        
        return min(1.0, score / max(1, matches)) if matches > 0 else 0.0
