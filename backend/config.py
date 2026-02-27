from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "AI Red Team Toolkit"
    debug: bool = False

    # 資料庫（預設 SQLite 本地開發）
    database_url: str = "sqlite:///./red_team.db"

    # Anthropic API
    anthropic_api_key: str = ""

    # OpenAI-compatible API（自架 LLM 用）
    openai_api_key: str = ""
    custom_llm_base_url: str = "http://localhost:11434/v1"
    custom_llm_api_key: str = ""

    # CORS
    cors_origins: list[str] = [
        "http://localhost:5175",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
