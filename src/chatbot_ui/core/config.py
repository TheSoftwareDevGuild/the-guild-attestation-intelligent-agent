from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    GOOGLE_API_KEY: str

    API_URL: str = "http://api:8000"  # Default for local Docker, override with env var for production

    model_config = SettingsConfigDict(env_file=".env")

config = Config()