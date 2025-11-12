"""
Tilly LLM Core - The Multi-Model Brain
Seamlessly switches between Gemini, DeepSeek, and local models
"""

import asyncio
try:
    import aiohttp  # type: ignore
except Exception:
    aiohttp = None  # type: ignore
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
import logging
from src.tilly.config.configuration_manager import ModelConfig, TillyConfigManager
from src.tilly.core.tilly_conversation_context import TillyContext

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    """Abstract base for all LLM providers"""
    
    @abstractmethod
    async def generate(self, prompt: str, context: TillyContext, **kwargs) -> List[str]:
        """Generate response candidates"""
        pass
    
    @abstractmethod  
    async def health_check(self) -> bool:
        """Check if the provider is available"""
        pass

class GeminiProvider(LLMProvider):
    """Google Gemini API integration"""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    async def generate(self, prompt: str, context: TillyContext, **kwargs) -> List[str]:
        """Generate using Gemini API"""
        if not self.config.api_key:
            raise ValueError("Gemini API key not configured")
        
        # Craft context-aware prompt
        system_prompt = self._build_system_prompt(context)
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nTilly:"
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/models/{self.config.model_name}:generateContent"
            headers = {"Content-Type": "application/json"}
            params = {"key": self.config.api_key}
            
            payload = {
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {
                    "temperature": self.config.temperature,
                    "maxOutputTokens": self.config.max_tokens,
                    "candidateCount": 3  # Multiple candidates for ethics filtering
                }
            }
            
            async with session.post(url, json=payload, headers=headers, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    candidates = []
                    for candidate in data.get("candidates", []):
                        if "content" in candidate and "parts" in candidate["content"]:
                            text = candidate["content"]["parts"][0].get("text", "")
                            candidates.append(text.strip())
                    return candidates or ["I'm having trouble generating a response right now."]
                else:
                    raise Exception(f"Gemini API error: {resp.status}")
    
    def _build_system_prompt(self, context: TillyContext) -> str:
        """Build context-aware system prompt"""
        base = "You are Tilly, an empathetic AI companion focused on mental wellness."
        
        if context.intent.value == "crisis":
            return f"{base} The user may be in crisis. Respond with compassion and include crisis resources."
        elif context.intent.value == "wellness": 
            return f"{base} The user needs therapeutic support. Use CBT techniques and validate their feelings."
        else:
            return f"{base} Have a natural, supportive conversation matching their communication style."
    
    async def health_check(self) -> bool:
        """Check if Gemini API is responsive"""
        try:
            test_candidates = await self.generate("Hello", TillyContext())
            return len(test_candidates) > 0
        except:
            return False

class DeepSeekProvider(LLMProvider):
    """DeepSeek API integration"""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.base_url = "https://api.deepseek.com/v1"
    
    async def generate(self, prompt: str, context: TillyContext, **kwargs) -> List[str]:
        """Generate using DeepSeek API"""
        # Implementation similar to Gemini but with DeepSeek's API format
        if not self.config.api_key:
            raise ValueError("DeepSeek API key not configured")
            
        # For now, return a placeholder - implement full API integration
        return [f"[DeepSeek Response] {prompt}"]
    
    async def health_check(self) -> bool:
        return True  # Placeholder

class TillyBrain:
    """The orchestrator that manages multiple LLM providers"""
    
    def __init__(self):
        self.config_manager = TillyConfigManager()
        self.providers: Dict[str, LLMProvider] = {}
        self._setup_providers()
    
    def _setup_providers(self):
        """Initialize all configured providers"""
        config = self.config_manager.config
        
        if config.primary_model.provider == "gemini":
            self.providers["gemini"] = GeminiProvider(config.primary_model)
        elif config.primary_model.provider == "deepseek":
            self.providers["deepseek"] = DeepSeekProvider(config.primary_model)
            
        if config.fallback_model:
            if config.fallback_model.provider == "gemini":
                self.providers["gemini_fallback"] = GeminiProvider(config.fallback_model)
            elif config.fallback_model.provider == "deepseek":
                self.providers["deepseek_fallback"] = DeepSeekProvider(config.fallback_model)
    
    async def generate_candidates(self, prompt: str, context: TillyContext) -> List[str]:
        """Generate response candidates with automatic fallback"""
        config = self.config_manager.config
        primary_provider = self.providers.get(config.primary_model.provider)
        
        if not primary_provider:
            raise ValueError(f"No provider configured for {config.primary_model.provider}")
        
        try:
            # Try primary provider first
            candidates = await primary_provider.generate(prompt, context)
            if candidates:
                return candidates
        except Exception as e:
            print(f"Primary provider failed: {e}")
        
        # Fall back to backup provider
        if config.fallback_model:
            fallback_provider = self.providers.get(f"{config.fallback_model.provider}_fallback")
            if fallback_provider:
                try:
                    return await fallback_provider.generate(prompt, context)
                except Exception as e:
                    print(f"Fallback provider failed: {e}")
        
        # Last resort: return a safe response
        return ["I'm having some technical difficulties right now. Let's try again in a moment."]
