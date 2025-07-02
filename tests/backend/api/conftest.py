import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.backend.main import app
from src.backend.database.db_connection import get_db  # IMPORTANTE

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def client(mock_db):
    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = lambda: (yield mock_db)
    return TestClient(app)
