from pydantic_settings import BaseSettings,SettingsConfigDict

class Config(BaseSettings):

    OPENAI_API_KEY: str
    GROQ_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    CO_API_KEY: str | None = None
    
    # Qdrant Cloud configuration
    QDRANT_URL: str = "http://localhost:6333"  # Default to local for development
    QDRANT_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env")

config=Config()