from pydantic_settings import BaseSettings,SettingsConfigDict

class Config(BaseSettings):

    OPENAI_API_KEY: str
    GROQ_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    
    # Qdrant Cloud configuration
    QDRANT_URL: str = "http://localhost:6333"  # Default to local for development
    QDRANT_API_KEY: str | None = None
    
    # Simple password authentication
    APP_PASSWORD: str = "changeme123"  # Change this in production

    model_config = SettingsConfigDict(env_file=".env")

config=Config()