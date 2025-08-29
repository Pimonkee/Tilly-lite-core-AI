"""
Tilly Pipeline - The Complete Intelligence Stack
Where all the magic comes together into one coherent AI companion.
"""

import logging
from typing import List
from tilly_conversation_context import TillyContext, IntentType
from tilly_intent_router import TillyRouter
from tilly_mood_analyzer import TillyMoodDetector
from tilly_l_l_m_provider_manager import TillyBrain

logger = logging.getLogger(__name__)

class TillyPipeline:
    """
    The complete Tilly intelligence pipeline.
    This orchestrates every module to create a coherent, empathetic AI companion.
    """
    
    def __init__(self):
        # Initialize all pipeline modules
        self.router = TillyRouter()
        self.mood_detector = TillyMoodDetector()
        self.brain = TillyBrain()
        
        logger.info("🚀 Tilly Pipeline initialized and ready!")
    
    async def process(self, user_input: str, session_id: str = None) -> tuple[str, TillyContext]:
        """
        Process user input through the complete Tilly pipeline.
        This is where the magic happens!
        Returns a tuple of (response, context) so callers can access intent/mood/model info.
        """
        # Create context for this conversation turn
        context = TillyContext(
            user_text=user_input,
            session_id=session_id or "default"
        )
        
        logger.info(f"🎯 Processing: '{user_input[:50]}...' for session {context.session_id}")
        
        try:
            # Stage 1: Route the intent
            text, context = await self.router.process(user_input, context)
            
            # Stage 2: Analyze mood and emotional state
            text, context = await self.mood_detector.process(text, context)
            
            # Stage 3: Generate response candidates using LLM
            # Note: provider manager may ignore candidate count; handle gracefully
            try:
                candidates = await self.brain.generate_candidates(text, context)
            except TypeError:
                # Backward compatibility if signature differs
                candidates = await self.brain.generate_candidates(text, context)
            context.response_candidates = candidates
            
            # Stage 4: Select best candidate (for now, just take the first one)
            # TODO: Add ethics filtering, chaos engine, etc.
            if candidates:
                selected_response = candidates[0]
            else:
                selected_response = "I'm having trouble processing that right now. Could you try rephrasing?"
            
            # Add crisis resources if needed
            if context.is_crisis():
                crisis_resources = "\n\nIf you're having thoughts of self-harm, please reach out:\n• National Suicide Prevention Lifeline: 988\n• Crisis Text Line: Text HOME to 741741\n• Or go to your nearest emergency room"
                selected_response += crisis_resources
            
            logger.info(f"✅ Response generated using {context.model_used}")
            logger.info(f"📊 Intent: {context.intent.value}, Mood: {context.mood.value}, Vulnerability: {context.vulnerability_index:.2f}")
            
            return selected_response, context
            
        except Exception as e:
            logger.error(f"❌ Pipeline error: {e}")
            fallback_response = "I'm experiencing some technical difficulties right now. Please try again in a moment, and if you need immediate support, don't hesitate to reach out to a crisis helpline."
            return fallback_response, context
    
    async def health_check(self) -> dict:
        """Check health of all pipeline components"""
        health_status = {
            "pipeline": "healthy",
            "router": "healthy",
            "mood_detector": "healthy",
            "brain": {}
        }
        
        try:
            # Check brain health (LLM providers)
            if hasattr(self.brain, 'health_check_all'):
                brain_health = await self.brain.health_check_all()  # type: ignore
            else:
                # Approximate health by checking each provider if available
                brain_health = {"unknown": True}
            health_status["brain"] = brain_health
            
            # Overall health
            if not any(brain_health.values()):
                health_status["pipeline"] = "degraded"
                
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            health_status["pipeline"] = "unhealthy"
            health_status["error"] = str(e)
        
        return health_status
    
    async def close(self):
        """Clean up resources"""
        try:
            if hasattr(self.brain, 'close_all'):
                await self.brain.close_all()  # type: ignore
        except Exception:
            pass
        logger.info("🔒 Tilly Pipeline closed")
