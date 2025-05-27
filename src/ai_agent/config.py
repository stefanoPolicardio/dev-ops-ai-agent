"""Configuration management for the AI Agent."""

import os
from typing import Optional

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Configuration settings for the AI Agent.
    
    Uses environment variables with type validation and defaults.
    """
    
    # Configure Pydantic to ignore extra fields
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # This will ignore unknown environment variables
    )
    
    # LLM Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    llm_model: str = Field(default="gpt-4", env="LLM_MODEL")
    llm_temperature: float = Field(default=0.7, env="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=1000, env="LLM_MAX_TOKENS")
    
    # Agent Configuration
    agent_name: str = Field(default="AI Assistant", env="AGENT_NAME")
    agent_description: str = Field(
        default="A helpful AI agent", env="AGENT_DESCRIPTION"
    )
    agent_max_memory_size: int = Field(default=100, env="AGENT_MAX_MEMORY_SIZE")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # API Configuration
    api_host: str = Field(default="localhost", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_debug: bool = Field(default=False, env="API_DEBUG")
    
    # Database Configuration
    database_url: Optional[str] = Field(default=None, env="DATABASE_URL")
    
    # Security
    secret_key: Optional[str] = Field(default=None, env="SECRET_KEY")


def get_config() -> Config:
    """Get configuration instance.
    
    Returns:
        Config: Configuration instance with environment variables loaded.
    """
    return Config() 