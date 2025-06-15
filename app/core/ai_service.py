"""
AI Service for Monk-AI
"""

import os
import asyncio
from typing import Dict, Any, List, Optional, Callable
import logging
import json
import time
import random

import backoff
from sqlalchemy.orm import Session
import openai
from openai import OpenAI
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

from app.core.config import settings
<<<<<<< HEAD
from app.crud.agent_log import AgentLogRepository
from app.models.agent_log import LogLevel
from app.models.agent_logs import AgentLog
=======
from app.crud.agent_log import LogLevel
>>>>>>> 3258ec8ed28032f9b41b5f58eb392e52109c83bb

logger = logging.getLogger(__name__)


class AIService:
    """Centralized AI service with multi-provider support and failover capabilities."""

    def __init__(self, session: Session):
        """
        Initializes the AIService.
        
        Args:
            session (Session): The database session.
        """
        self.session = session
        self.agent_log_repo = AgentLogRepository()
        
        # Initialize providers
        self._init_providers()
        
        # Provider priority order (Gemini first, then OpenAI)
        self.providers = [
            self._get_gemini_response,
            self._get_openai_response,
        ]

    def _init_providers(self):
        """Initialize AI providers with proper error handling."""
        try:
            # Initialize OpenAI client with minimal parameters
            if settings.OPENAI_API_KEY:
                self.openai_client = OpenAI(
                    api_key=settings.OPENAI_API_KEY
                )
                logger.info("✅ OpenAI client initialized successfully")
            else:
                self.openai_client = None
                logger.warning("⚠️ OpenAI API key not found")
        except Exception as e:
            logger.error(f"❌ Failed to initialize OpenAI client: {e}")
            self.openai_client = None
        
        try:
            # Initialize Gemini
            if settings.GOOGLE_API_KEY:
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
                logger.info("✅ Gemini client initialized successfully")
            else:
                self.gemini_model = None
                logger.warning("⚠️ Google API key not found")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini client: {e}")
            self.gemini_model = None

    async def generate_text_with_failover(
        self,
        prompt: str,
        agent_id: int = 1,
        task_id: int = 1,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate text with automatic failover between providers."""
        
        for i, provider in enumerate(self.providers):
            try:
                logger.info(f"🔄 Attempting provider {i+1}/{len(self.providers)}")
                result = await provider(prompt, temperature, max_tokens)
                
                # Log successful generation
                await self._log_generation(
                    agent_id=agent_id,
                    task_id=task_id,
                    prompt=prompt[:200] + "..." if len(prompt) > 200 else prompt,
                    response=result.get('content', '')[:200] + "..." if len(result.get('content', '')) > 200 else result.get('content', ''),
                    provider=f"provider_{i+1}",
                    success=True
                )
                
                return result
                
            except Exception as e:
                logger.warning(f"⚠️ Provider {i+1} failed: {str(e)}")
                if i == len(self.providers) - 1:  # Last provider
                    # Log failed generation
                    await self._log_generation(
                        agent_id=agent_id,
                        task_id=task_id,
                        prompt=prompt[:200] + "..." if len(prompt) > 200 else prompt,
                        response="",
                        provider="all_failed",
                        success=False,
                        error_message=str(e)
                    )
                    
                    # Return fallback response
                    return {
                        'content': self._get_fallback_response(prompt),
                        'provider': 'fallback',
                        'error': str(e)
                    }
                continue
    
    async def generate_text(
        self,
        prompt: str,
        agent_id: int = 1,
        task_id: int = 1,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate text using the primary method with failover."""
        return await self.generate_text_with_failover(
            prompt=prompt,
            agent_id=agent_id,
            task_id=task_id,
            max_tokens=max_tokens,
            temperature=temperature
        )

    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    async def _get_gemini_response(self, prompt: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Get response from Google Gemini."""
        if not self.gemini_model:
            raise Exception("Gemini model not initialized")
        
        try:
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            
            return {
                'content': response.text,
                'provider': 'gemini',
                'model': 'gemini-1.5-flash-latest'
            }
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    async def _get_openai_response(self, prompt: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Get response from OpenAI."""
        if not self.openai_client:
            raise Exception("OpenAI client not initialized")
        
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                'content': response.choices[0].message.content,
                'provider': 'openai',
                'model': 'gpt-4o'
            }
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    def _get_fallback_response(self, prompt: str) -> str:
        """Generate a fallback response when all providers fail."""
        fallback_responses = [
            "I apologize, but I'm currently experiencing technical difficulties. Please try again later.",
            "The AI service is temporarily unavailable. Your request has been noted and will be processed when service is restored.",
            "I'm unable to process your request at the moment due to service limitations. Please check back soon.",
            "Technical issues are preventing me from generating a response right now. Please retry your request.",
            "The AI providers are currently unavailable. This is a temporary issue that should resolve shortly."
        ]
        
        # Add some context-aware fallbacks based on prompt content
        if "code" in prompt.lower():
            fallback_responses.extend([
                "I'm unable to analyze the code at the moment. Please ensure your code follows best practices and try again later.",
                "Code analysis is temporarily unavailable. Consider reviewing your code manually for now."
            ])
        elif "review" in prompt.lower():
            fallback_responses.extend([
                "The review service is temporarily unavailable. Please perform a manual review for now.",
                "I cannot provide a detailed review at this time. Please check back later."
            ])
        elif "test" in prompt.lower():
            fallback_responses.extend([
                "Test generation is currently unavailable. Consider writing tests manually following your project's testing patterns.",
                "The testing service is temporarily down. Please create tests based on your existing test suite structure."
            ])
        
        return random.choice(fallback_responses)

    async def _log_generation(
        self,
        agent_id: int,
        task_id: int,
        prompt: str,
        response: str,
        provider: str,
        success: bool,
        error_message: Optional[str] = None
    ):
        """Log AI generation attempts to database."""
        try:
            log_entry = AgentLog(
                agent_id=agent_id,
                task_id=task_id,
                action="ai_generation",
                details={
                    "prompt_preview": prompt,
                    "response_preview": response,
                    "provider": provider,
                    "success": success,
                    "error": error_message,
                    "timestamp": time.time()
                },
                status="completed" if success else "failed"
            )
            
            self.session.add(log_entry)
            await asyncio.to_thread(self.session.commit)
            
        except Exception as e:
            logger.error(f"Failed to log AI generation: {e}")
            # Don't raise here to avoid breaking the main flow

    async def generate_json_output(self, prompt: str, output_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a JSON output from a prompt using a specified schema.
        This is a placeholder and needs to be implemented with proper failover.
        """
        # For now, this just uses OpenAI. It should be updated to use the failover logic.
        logger.info("Generating JSON output with OpenAI...")
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that always responds in JSON format.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object", "schema": output_schema},
            )
            json_response = json.loads(response.choices[0].message.content)
            logger.info("Successfully generated JSON from OpenAI.")
            return json_response
        except Exception as e:
            logger.error(f"Error generating JSON from OpenAI: {e}", exc_info=True)
            raise


# Create a default instance for backward compatibility
# Note: This will need a database session when used
ai_service = None  # Will be initialized with a session when needed