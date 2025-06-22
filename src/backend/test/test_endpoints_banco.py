import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

def test_test_db_conexao_sucesso(client, mock_db):
    """Testa o endpoint de teste de conexão com o banco de dados."""
    # Configurar mock para simular conexão bem-sucedida
    with patch('src.backend.api.endpoints_banco.get_db', return_value=mock_db):
        # Fazer requisição
        response = client.get("/test-db")
        
        # Verificar resultado
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "Conectado ao PostgreSQL!"

@patch('src.backend.api.endpoints_banco.get_db')
def test_test_db_erro_conexao(mock_get_db, client):
    """Testa o endpoint de teste de conexão com erro no banco de dados."""
    # Configurar mock para simular erro de conexão
    mock_get_db.side_effect = Exception("Erro de conexão com o banco de dados")
    
    # Fazer requisição
    response = client.get("/test-db")
    
    # Verificar resultado
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
