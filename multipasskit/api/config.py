from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets


class Settings(BaseSettings):
    APP_NAME: str = "Multipass API"
    MULTIPASS_API_VERSION: str = "v0.1.0"
    REDIS_URL: str = "redis://localhost:6379"
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    FIRST_SUPERUSER: str = "multipassadmin"
    FIRST_SUPERUSER_PASSWORD: str = "multipassadmin"

    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()