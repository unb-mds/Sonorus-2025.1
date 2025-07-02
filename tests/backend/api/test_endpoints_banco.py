import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

def test_test_db_conexao_sucesso(client, mock_db):
    """Testa o endpoint de teste de conexão com o banco de dados."""
    # Configurar mock para simular conexão bem-sucedida
    with patch('src.backend.api.endpoints_banco.get_db', return_value=mock_db):
        # Fazer requisição
        response = client.get("/api/test-db")
        
        # Verificar resultado
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "Conectado ao PostgreSQL!"

def test_test_db_erro_conexao(client):
    from src.backend.database.db_connection import get_db
    def erro_get_db():
        raise Exception("Erro de conexão com o banco de dados")
    client.app.dependency_overrides[get_db] = erro_get_db

    with pytest.raises(Exception) as excinfo:
        client.get("/api/test-db")
    assert "Erro de conexão com o banco de dados" in str(excinfo.value)
