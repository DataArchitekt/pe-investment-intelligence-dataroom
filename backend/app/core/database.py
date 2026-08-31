from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import PROJECT_ROOT, settings


def _database_url() -> str:
    """Resolve local SQLite paths from the repository root."""
    if settings.database_url.startswith("sqlite:///./"):
        relative_path = settings.database_url.removeprefix("sqlite:///./")
        return f"sqlite:///{(PROJECT_ROOT / relative_path).as_posix()}"
    return settings.database_url


database_url = _database_url()
connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
engine = create_engine(database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def ensure_schema() -> None:
    """Apply the small additive Day 1 update without adding migration tooling."""
    if not database_url.startswith("sqlite") or "documents" not in inspect(engine).get_table_names():
        return
    columns = {column["name"] for column in inspect(engine).get_columns("documents")}
    additions = {
        "file_size": "INTEGER NOT NULL DEFAULT 0",
        "content_type": "VARCHAR(255) NOT NULL DEFAULT 'application/octet-stream'",
        "original_file_name": "VARCHAR(255) NOT NULL DEFAULT ''",
        "page_count": "INTEGER NOT NULL DEFAULT 0",
        "processing_error": "TEXT",
    }
    with engine.begin() as connection:
        for name, definition in additions.items():
            if name not in columns:
                connection.execute(text(f"ALTER TABLE documents ADD COLUMN {name} {definition}"))


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
