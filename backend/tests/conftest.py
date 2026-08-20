import os
import tempfile
from pathlib import Path

test_database = Path(tempfile.gettempdir()) / "pe_dataroom_test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{test_database.as_posix()}"

import pytest
from fastapi.testclient import TestClient

from app.core.database import Base, SessionLocal, engine
from app.main import app


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        yield client
    Base.metadata.drop_all(bind=engine)
