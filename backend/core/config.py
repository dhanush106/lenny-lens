from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "LennyLens API"
    ENVIRONMENT: str = "development"
    API_PORT: int = 8000
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    LLM_PROVIDER: str = "ollama"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4.1-mini"
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-haiku-20240307"
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "qwen3.5:2b"
    OLLAMA_TIMEOUT_SECONDS: float = 180.0
    EMBEDDING_PROVIDER: str = "ollama"
    OLLAMA_EMBEDDING_MODEL: str = "all-minilm"
    EMBEDDING_DIMENSIONS: int = 384
    RETRIEVAL_MODE: str = "lexical"
    RETRIEVAL_TOP_K: int = 8
    RETRIEVAL_MIN_SCORE: float = 0.0
    RETRIEVAL_MAX_PER_TRANSCRIPT: int = 2
    GROUNDING_MIN_CONFIDENCE: float = 0.35

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

settings = Settings()
