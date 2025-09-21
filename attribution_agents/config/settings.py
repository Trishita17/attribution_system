from pydantic_settings import BaseSettings
import os
from pathlib import Path

class Settings(BaseSettings):
    # Snowflake Connection
    SNOWFLAKE_ACCOUNT: str
    SNOWFLAKE_USER: str
    SNOWFLAKE_PASSWORD: str
    SNOWFLAKE_DATABASE: str = "MULTI_AGENT_ATTRIBUTION"
    SNOWFLAKE_SCHEMA: str = "ATTRIBUTION_SCHEMA"
    AUTHENTICATOR: str = "externalbrowser"
    
    # LLM Configuration
    ANTHROPIC_API_KEY: str
    LLM_MODEL: str = "claude-3-haiku-20240307"
    LLM_PROVIDER: str = "anthropic"
    
    # MCP Configuration
    MCP_SERVER_PORT: int = 8080
    
    class Config:
        env_file = Path(__file__).parent.parent / ".env"

settings = Settings()