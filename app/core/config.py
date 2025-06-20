from typing import List, Optional, Union, Dict, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Monk AI"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "INSECURE_DEVELOPMENT_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    ALGORITHM: str = "HS256"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database
    DATABASE_URI: str = os.getenv("DATABASE_URI", "sqlite:///./monk_ai.db")
    
    # Redis cache settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_CACHE_EXPIRE_SECONDS: int = int(os.getenv("REDIS_CACHE_EXPIRE_SECONDS", "3600"))
    
    # AI Model Settings (Legacy)
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "gpt-4")
    AI_TEMPERATURE: float = float(os.getenv("AI_TEMPERATURE", "0.7"))
    AI_MAX_TOKENS: int = int(os.getenv("AI_MAX_TOKENS", "1000"))
    
    # Multi-Provider AI API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_GEMINI_API_KEY", "")))
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    NOVITA_API_KEY: str = os.getenv("NOVITA_API_KEY", "")
    
    # GitHub Integration
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    # Agent Settings
    MAX_CONCURRENT_AGENTS: int = int(os.getenv("MAX_CONCURRENT_AGENTS", "5"))
    AGENT_TIMEOUT_SECONDS: int = int(os.getenv("AGENT_TIMEOUT_SECONDS", "300"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Storage
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./data")
    
    # Define config for settings
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"
    )

# Create global settings object
settings = Settings() 