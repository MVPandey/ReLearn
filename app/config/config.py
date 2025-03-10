from pydantic_settings import BaseSettings
import os


class AppSettings(BaseSettings):
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LLM_API_BASE_URL: str = os.getenv("LLM_API_BASE_URL")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME")
    EMBEDDING_API_BASE_URL: str = os.getenv("EMBEDDING_API_BASE_URL")
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY")
    EMBEDDING_API_KEY: str = os.getenv("EMBEDDING_API_KEY")
    POSTGRES_DB_NAME: str = os.getenv("POSTGRES_DB_NAME", "postgres")
    POSTGRES_DB_USER: str = os.getenv("POSTGRES_DB_USER", "postgres")
    POSTGRES_DB_PASSWORD: str = os.getenv("POSTGRES_DB_PASSWORD", "postgres")
    POSTGRES_DB_HOST: str = os.getenv("POSTGRES_DB_HOST", "localhost")
    POSTGRES_DB_PORT: int = os.getenv("POSTGRES_DB_PORT", 5432)

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_db_user}:{self.postgres_db_password}@{self.postgres_db_host}:{self.postgres_db_port}/{self.postgres_db_name}"


app_settings = AppSettings()
