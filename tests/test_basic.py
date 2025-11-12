"""
Basic tests for Tilly AI components
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tilly.core.tilly_conversation_context import TillyContext, IntentType, MoodState
from tilly.core.tilly_intent_router import TillyRouter
from tilly.core.tilly_mood_analyzer import TillyMoodDetector


class TestConversationContext:
    """Test conversation context functionality"""
    
    def test_context_creation(self):
        """Test creating a basic context"""
        context = TillyContext(user_text="Hello")
        assert context.user_text == "Hello"
        assert context.intent == IntentType.UNKNOWN
        assert context.mood == MoodState.NEUTRAL
    
    def test_crisis_detection(self):
        """Test crisis detection method"""
        context = TillyContext(crisis_level=0.9)
        assert context.is_crisis()
        
        context2 = TillyContext(intent=IntentType.CRISIS)
        assert context2.is_crisis()
    
    def test_needs_gentle_care(self):
        """Test gentle care detection"""
        context = TillyContext(mood=MoodState.VULNERABLE)
        assert context.needs_gentle_care()
        
        context2 = TillyContext(vulnerability_index=0.8)
        assert context2.needs_gentle_care()


@pytest.mark.asyncio
class TestIntentRouter:
    """Test intent routing functionality"""
    
    async def test_chat_intent(self):
        """Test casual chat intent detection"""
        router = TillyRouter()
        context = TillyContext()
        
        text, updated_context = await router.process("Hello, how are you?", context)
        assert updated_context.intent == IntentType.CHAT
    
    async def test_wellness_intent(self):
        """Test wellness intent detection"""
        router = TillyRouter()
        context = TillyContext()
        
        text, updated_context = await router.process("I'm feeling really depressed", context)
        assert updated_context.intent == IntentType.WELLNESS
        assert updated_context.vulnerability_index > 0
    
    async def test_crisis_intent(self):
        """Test crisis intent detection"""
        router = TillyRouter()
        context = TillyContext()
        
        text, updated_context = await router.process("I want to kill myself", context)
        assert updated_context.intent == IntentType.CRISIS
        assert updated_context.crisis_level > 0.7


@pytest.mark.asyncio
class TestMoodAnalyzer:
    """Test mood analysis functionality"""
    
    async def test_positive_mood(self):
        """Test positive mood detection"""
        analyzer = TillyMoodDetector()
        context = TillyContext()
        
        text, updated_context = await analyzer.process("I'm feeling great today!", context)
        assert updated_context.mood == MoodState.POSITIVE
    
    async def test_vulnerable_mood(self):
        """Test vulnerable mood detection"""
        analyzer = TillyMoodDetector()
        context = TillyContext()
        
        text, updated_context = await analyzer.process("I feel so hopeless and lost", context)
        assert updated_context.mood == MoodState.VULNERABLE
        assert updated_context.vulnerability_index > 0
    
    async def test_neutral_mood(self):
        """Test neutral mood detection"""
        analyzer = TillyMoodDetector()
        context = TillyContext()
        
        text, updated_context = await analyzer.process("What's the weather like?", context)
        # Should default to neutral for ambiguous text
        assert updated_context.mood in [MoodState.NEUTRAL, MoodState.POSITIVE]


def test_imports():
    """Test that all core modules can be imported"""
    from tilly.core import tilly_conversation_context
    from tilly.core import tilly_intent_router
    from tilly.core import tilly_mood_analyzer
    from tilly.core import tilly_intelligence_pipeline
    from tilly.core import tilly_l_l_m_provider_manager
    from tilly.config import configuration_manager
    from tilly.config import path_management
    
    assert True  # If we got here, imports succeeded


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
