"""
Core configuration module.
Handles environment variables and application settings.
"""
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class Settings:
    """Application settings."""
    
    XAI_API_KEY: str = os.getenv("XAI_API_KEY", "")
    PREVMET_API_URL = os.getenv("PREVMET_API_URL", "")
    PREVMET_API_ALERTS_URL = os.getenv("PREVMET_API_ALERTS_URL", "")
    DEFAULT_MODEL: str = "grok-beta"
    DEFAULT_TEMPERATURE: float = 0.7
    
    # API Configuration
    API_TITLE: str = "Weather AI Agent"
    API_DESCRIPTION: str = "A FastAPI application using LangChain with Grok models"
    API_VERSION: str = "1.0.0"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = False


settings = Settings()
