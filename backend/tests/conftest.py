import os
import tempfile
from pathlib import Path

test_database = Path(tempfile.gettempdir()) / "pe_dataroom_test.db"
test_storage = Path(tempfile.gettempdir()) / "pe_dataroom_test_documents"
os.environ["DATABASE_URL"] = f"sqlite:///{test_database.as_posix()}"
os.environ["DOCUMENT_STORAGE_PATH"] = str(test_storage)

import pytest
from fastapi.testclient import TestClient

from app.core.database import Base, SessionLocal, engine
from app.main import app


@pytest.fixture
def client():
    if test_storage.exists():
        import shutil
        shutil.rmtree(test_storage)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        yield client
    Base.metadata.drop_all(bind=engine)
    if test_storage.exists():
        import shutil
        shutil.rmtree(test_storage)
