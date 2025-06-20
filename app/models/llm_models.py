"""
LLM Models Module
================
Supports multiple LLM providers including OpenAI and Google Gemini
"""

import os
import asyncio
import json
from typing import List, Dict, Any, Optional, Union
from abc import ABC, abstractmethod
import openai
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    async def generate_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate completion from messages"""
        pass
    
    @abstractmethod
    async def generate_structured_output(self, messages: List[Dict[str, str]], schema: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Generate structured output based on schema"""
        pass

class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
    
    async def generate_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate completion using OpenAI"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 2000)
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def generate_structured_output(self, messages: List[Dict[str, str]], schema: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Generate structured output using OpenAI function calling"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                functions=[{
                    "name": "structured_response",
                    "description": "Generate structured response",
                    "parameters": schema
                }],
                function_call={"name": "structured_response"},
                temperature=kwargs.get('temperature', 0.3)
            )
            
            function_call = response.choices[0].message.function_call
            return json.loads(function_call.arguments)
        except Exception as e:
            raise Exception(f"OpenAI structured output error: {str(e)}")

class GeminiProvider(BaseLLMProvider):
    """Google Gemini provider"""
    
    def __init__(self, model: str = "gemini-2.5-flash-preview"):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed. Install with: pip install google-generativeai")
        
        self.model = model
        api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)
    
    async def generate_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate completion using Gemini"""
        try:
            # Convert OpenAI format to Gemini format
            prompt = self._convert_messages_to_prompt(messages)
            
            response = await self.client.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=kwargs.get('temperature', 0.7),
                    max_output_tokens=kwargs.get('max_tokens', 2000)
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    async def generate_structured_output(self, messages: List[Dict[str, str]], schema: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Generate structured output using Gemini"""
        try:
            # Add schema instruction to prompt
            schema_prompt = f"\nPlease respond in JSON format following this schema: {json.dumps(schema, indent=2)}"
            messages = messages.copy()
            messages[-1]["content"] += schema_prompt
            
            prompt = self._convert_messages_to_prompt(messages)
            
            response = await self.client.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=kwargs.get('temperature', 0.3),
                    max_output_tokens=kwargs.get('max_tokens', 2000)
                )
            )
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: try to parse the entire response as JSON
                return json.loads(response_text)
                
        except Exception as e:
            raise Exception(f"Gemini structured output error: {str(e)}")
    
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI message format to Gemini prompt format"""
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        return "\n\n".join(prompt_parts)

class LLMFactory:
    """Factory for creating LLM providers"""
    
    @staticmethod
    def create_provider(provider: str = "openai", model: str = None) -> BaseLLMProvider:
        """Create LLM provider based on configuration"""
        provider = provider.lower()
        
        if provider == "openai":
            model = model or "gpt-4o"
            return OpenAIProvider(model)
        elif provider == "gemini":
            model = model or "gemini-2.5-flash-preview"
            return GeminiProvider(model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    @staticmethod
    def get_available_providers() -> List[str]:
        """Get list of available providers"""
        providers = ["openai"]
        if GEMINI_AVAILABLE:
            providers.append("gemini")
        return providers

# Global LLM provider instance
_llm_provider: Optional[BaseLLMProvider] = None

def get_llm_provider() -> BaseLLMProvider:
    """Get the current LLM provider"""
    global _llm_provider
    if _llm_provider is None:
        # Default to OpenAI, fallback to Gemini if available
        provider_name = os.getenv("LLM_PROVIDER", "openai")
        model_name = os.getenv("LLM_MODEL")
        _llm_provider = LLMFactory.create_provider(provider_name, model_name)
    return _llm_provider

def set_llm_provider(provider: str, model: str = None):
    """Set the global LLM provider"""
    global _llm_provider
    _llm_provider = LLMFactory.create_provider(provider, model)

async def generate_completion(messages: List[Dict[str, str]], **kwargs) -> str:
    """Generate completion using the current provider"""
    provider = get_llm_provider()
    return await provider.generate_completion(messages, **kwargs)

async def generate_structured_output(messages: List[Dict[str, str]], schema: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """Generate structured output using the current provider"""
    provider = get_llm_provider()
    return await provider.generate_structured_output(messages, schema, **kwargs) 