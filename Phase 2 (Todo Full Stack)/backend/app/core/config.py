from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore"
    )

    PROJECT_NAME: str = "Todo API"
    BETTER_AUTH_SECRET: str = "dev-secret"
    BETTER_AUTH_URL: str = "http://localhost:3000"
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

settings = Settings()
