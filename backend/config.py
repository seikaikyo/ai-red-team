from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "AI Red Team Toolkit"
    debug: bool = False

    # 應用程式 API Key（保護寫入/執行端點）
    app_api_key: str = ""

    # 跳過 API Key 驗證。只給本機開發用，正式部署維持 False。
    # 未設 app_api_key 且未開此旗標時，寫入/執行端點一律回 503。
    allow_insecure_auth: bool = False

    # 允許 base_url 指向私網與 loopback。自架 LLM（Ollama / vLLM /
    # LM Studio）在本機開發時需要，正式部署維持 False 以防 SSRF。
    allow_private_base_url: bool = False

    # 資料庫（本地 SQLite，正式環境用 Neon PostgreSQL）
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

    # Rate Limiting
    rate_limit: str = "30/minute"
    rate_limit_test: str = "10/minute"


@lru_cache
def get_settings() -> Settings:
    return Settings()
