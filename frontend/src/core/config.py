from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    API_URL: str = "http://backend:8000"  # Default for local Docker, override with env var for production

    model_config = SettingsConfigDict(env_file=".env")

config = Config()