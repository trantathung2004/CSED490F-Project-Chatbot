from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Application configuration settings
    """
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Raspberry Pi Chatbot Server"
    VERSION: str = "1.0.0"
    
    # Ollama Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_DEFAULT_MODEL: str = "llama3.2"
    OLLAMA_TIMEOUT: int = 120  # seconds
    OLLAMA_KEEP_ALIVE: str = "5m"  # Keep model loaded for 5 minutes
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",
        "*"  # Allow all origins for development
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()