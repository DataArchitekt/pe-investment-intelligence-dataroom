from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Application settings. Azure values remain optional until future phases."""

    database_url: str = "sqlite:///./data/app.db"
    frontend_origin: str = "http://localhost:5173"
    document_storage_path: str = "./data/documents"
    document_max_upload_size_mb: int = 25
    document_chunk_size_words: int = 1000
    document_chunk_overlap_words: int = 150

    azure_storage_account: str | None = None
    azure_storage_container: str | None = None
    azure_storage_connection_string: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_api_key: str | None = None
    azure_openai_chat_deployment: str | None = None
    azure_openai_embedding_deployment: str | None = None
    azure_search_endpoint: str | None = None
    azure_search_api_key: str | None = None
    azure_search_index: str | None = None

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
