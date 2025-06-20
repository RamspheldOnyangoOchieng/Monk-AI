import logging
import os
import json
import hashlib
from typing import Dict, List, Optional, Any, Union
import httpx
import asyncio
import redis.asyncio as redis
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

class AIClient:
    """
    Client for interacting with AI models (OpenAI, HuggingFace, etc.).
    Features:
    - Retry logic for API errors
    - Response caching with Redis
    - Multiple model provider support
    - Async implementation for non-blocking operations
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None,
        cache_enabled: bool = True
    ):
        # Use provided values or defaults from settings
        self.api_key = api_key or settings.AI_API_KEY
        self.model = model or settings.AI_MODEL
        self.temperature = temperature if temperature is not None else settings.AI_TEMPERATURE
        self.max_tokens = max_tokens or settings.AI_MAX_TOKENS
        self.cache_enabled = cache_enabled
        
        # Initialize Redis connection if caching is enabled
        if self.cache_enabled:
            self.redis = redis.from_url(settings.REDIS_URL)
        
        # Validate API key
        if not self.api_key:
            logger.warning("No API key provided for AI client")
    
    async def _get_from_cache(self, cache_key: str) -> Optional[str]:
        """Attempt to get a response from cache."""
        if not self.cache_enabled:
            return None
            
        try:
            cached_response = await self.redis.get(cache_key)
            if cached_response:
                logger.info(f"Cache hit for key: {cache_key[:10]}...")
                return cached_response.decode('utf-8')
        except Exception as e:
            logger.warning(f"Error accessing cache: {str(e)}")
        
        return None
    
    async def _save_to_cache(self, cache_key: str, value: str, expire_seconds: int = None) -> None:
        """Save a response to the cache."""
        if not self.cache_enabled:
            return
            
        try:
            expire_seconds = expire_seconds or settings.REDIS_CACHE_EXPIRE_SECONDS
            await self.redis.setex(
                cache_key,
                expire_seconds,
                value
            )
            logger.debug(f"Saved response to cache with key: {cache_key[:10]}...")
        except Exception as e:
            logger.warning(f"Error saving to cache: {str(e)}")
    
    def _generate_cache_key(self, prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        """Generate a deterministic cache key for the request."""
        # Create a unique key based on request parameters
        key_data = {
            "prompt": prompt,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        key_json = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_json.encode('utf-8')).hexdigest()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, httpx.ConnectTimeout))
    )
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text using the configured AI model with retries and caching.
        
        Args:
            prompt: The input prompt for the AI model
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            Generated text response
        """
        # Determine final parameters
        model = kwargs.get("model", self.model)
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        skip_cache = kwargs.get("skip_cache", False)

        # Try to get from cache unless skip_cache is True
        if not skip_cache:
            cache_key = self._generate_cache_key(prompt, model, temperature, max_tokens)
            cached_response = await self._get_from_cache(cache_key)
            if cached_response:
                return cached_response

        # Not in cache, make API call
        try:
            logger.debug(f"Sending request to AI model: {model}")
            
            # Different handling based on model provider
            if model.startswith("gpt"):
                # OpenAI API
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": model,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": temperature,
                            "max_tokens": max_tokens
                        }
                    )
                    response.raise_for_status()
                    result = response.json()
                    text_response = result["choices"][0]["message"]["content"]
                    
            elif model.startswith("claude"):
                # Anthropic API
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": self.api_key,
                            "anthropic-version": "2023-06-01",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": model,
                            "messages": [{"role": "user", "content": prompt}],
                            "max_tokens": max_tokens,
                            "temperature": temperature
                        }
                    )
                    response.raise_for_status()
                    result = response.json()
                    text_response = result["content"][0]["text"]
            
            else:
                # Generic fallback - just return mock response for demo
                logger.warning(f"Unsupported model: {model}, returning mock response")
                text_response = f"This is a mock response to: {prompt[:30]}..."
            
            # Cache the response for future use
            if not skip_cache:
                await self._save_to_cache(cache_key, text_response)
                
            return text_response
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during API call: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error during API call: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error calling AI API: {str(e)}")
            return f"Error: {str(e)}"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, httpx.ConnectTimeout))
    )
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts with retry logic.
        
        Args:
            texts: List of text inputs to generate embeddings for
            
        Returns:
            List of embedding vectors
        """
        try:
            # OpenAI embeddings API
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/embeddings",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "text-embedding-ada-002",
                        "input": texts
                    }
                )
                response.raise_for_status()
                result = response.json()
                embeddings = [item["embedding"] for item in result["data"]]
                return embeddings
                
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            return []


# Example usage
async def example_usage():
    # Initialize AI client
    ai_client = AIClient()
    
    # Generate text
    response = await ai_client.generate_text("Explain the concept of AI agents in 3 sentences.")
    print(f"AI Response: {response}")
    
    # Generate embeddings
    embeddings = await ai_client.generate_embeddings(["AI agent", "Machine learning"])
    print(f"Generated {len(embeddings)} embeddings") 