"""
Tilly Mood Detector - The Emotional Intelligence Engine
Reads the emotional undertones in human communication with unprecedented accuracy.
"""

from typing import Dict, Any
from tilly_conversation_context import TillyContext, MoodState
import logging

logger = logging.getLogger(__name__)

class TillyMoodDetector:
    """
    The Mood Detector is Tilly's emotional radar - it feels what humans feel
    and adjusts the entire pipeline accordingly.
    """
    
    def __init__(self):
        self.name = "mood_detector"
        
        # Emotional lexicon with intensity weights
        self.mood_lexicon = {
            MoodState.VULNERABLE: {
                "high": ["devastated", "hopeless", "suicidal", "worthless", "broken"],
                "medium": ["sad", "depressed", "anxious", "overwhelmed", "lost"],
                "low": ["down", "worried", "tired", "stressed", "uncertain"]
            },
            MoodState.POSITIVE: {
                "high": ["ecstatic", "amazing", "incredible", "fantastic", "thrilled"],
                "medium": ["happy", "great", "excited", "wonderful", "pleased"],
                "low": ["good", "nice", "okay", "fine", "alright"]
            },
            MoodState.AGITATED: {
                "high": ["furious", "enraged", "livid", "outraged"],
                "medium": ["angry", "frustrated", "annoyed", "upset"],
                "low": ["irritated", "bothered", "miffed"]
            }
        }
        
        # Emotional amplifiers and dampeners
        self.amplifiers = ["very", "extremely", "incredibly", "absolutely", "completely"]
        self.dampeners = ["a bit", "somewhat", "kind of", "sort of", "maybe"]
        
    async def process(self, text: str, context: TillyContext) -> tuple[str, TillyContext]:
        """Analyze emotional landscape of the text"""
        logger.info(f"Mood analysis for: {text[:50]}...")
        
        mood_analysis = self._analyze_emotional_landscape(text)
        context.mood = mood_analysis["dominant_mood"]
        context.vulnerability_index = max(context.vulnerability_index, mood_analysis["vulnerability_score"])
        
        # Store detailed mood analysis in metadata
        context.metadata["mood_analysis"] = mood_analysis
        
        logger.info(f"Detected mood: {context.mood}, vulnerability: {context.vulnerability_index:.2f}")
        
        return text, context.update_stage("mood_detected")
    
    def _analyze_emotional_landscape(self, text: str) -> Dict[str, Any]:
        """Perform deep emotional analysis of the text"""
        text_lower = text.lower()
        
        mood_scores = {
            MoodState.VULNERABLE: 0.0,
            MoodState.POSITIVE: 0.0,
            MoodState.AGITATED: 0.0,
            MoodState.NEUTRAL: 0.5  # Default baseline
        }
        
        # Analyze each mood category
        for mood_state, intensity_dict in self.mood_lexicon.items():
            for intensity, words in intensity_dict.items():
                for word in words:
                    if word in text_lower:
                        base_score = {"high": 0.9, "medium": 0.6, "low": 0.3}[intensity]
                        
                        # Apply amplifiers and dampeners
                        if any(amp in text_lower for amp in self.amplifiers):
                            base_score = min(1.0, base_score * 1.3)
                        elif any(damp in text_lower for damp in self.dampeners):
                            base_score *= 0.7
                            
                        mood_scores[mood_state] = max(mood_scores[mood_state], base_score)
        
        # Determine dominant mood
        dominant_mood = max(mood_scores.items(), key=lambda x: x[1])[0]
        
        # Calculate vulnerability score
        vulnerability_score = mood_scores[MoodState.VULNERABLE]
        if mood_scores[MoodState.AGITATED] > 0.6:
            vulnerability_score += 0.2  # Agitation increases vulnerability
            
        return {
            "dominant_mood": dominant_mood,
            "vulnerability_score": min(1.0, vulnerability_score),
            "mood_scores": mood_scores
        }
