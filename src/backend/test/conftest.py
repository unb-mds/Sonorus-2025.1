import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import MagicMock, patch

from src.backend.main import app
from src.backend.database.db_connection import get_db
from src.backend.models.sqlalchemy import Base

# Criar um banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def client():
    """
    Cria um cliente de teste para a API FastAPI com banco de dados mockado.
    """
    # Sobrescreve a dependência get_db para usar o banco de dados de teste
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    
    # Cria um cliente de teste
    with TestClient(app) as test_client:
        yield test_client
    
    # Limpa as substituições após o teste
    app.dependency_overrides.clear()

@pytest.fixture
def mock_db():
    """
    Retorna uma sessão de banco de dados mockada para testes unitários.
    """
    return MagicMock()
