import io
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from fastapi import UploadFile
from fastapi.testclient import TestClient

@patch('src.backend.api.endpoints_voz.validar_token_temporario')
@patch('src.backend.api.endpoints_voz.registrar_embedding_voz')
def test_registrar_voz_sucesso(mock_registrar_embedding, mock_validar_token, client):
    """Testa o registro de voz com sucesso."""
    # Configurar mocks
    usuario_mock = MagicMock()
    usuario_mock.id = 1
    usuario_mock.email = "teste@example.com"
    mock_validar_token.return_value = usuario_mock
    
    embedding_mock = np.array([0.1, 0.2, 0.3])
    mock_registrar_embedding.return_value = embedding_mock
    
    # Preparar arquivo de áudio simulado
    test_file = io.BytesIO(b"test audio content")
    
    # Fazer requisição
    response = client.post(
        "/api/registrar-voz",
        files={"arquivo": ("test.wav", test_file, "audio/wav")},
        headers={"Authorization": "Bearer token_teste"}
    )
    
    # Verificar resultado
    assert response.status_code == 200
    data = response.json()
    assert "mensagem" in data
    assert "embedding" in data
    assert data["mensagem"] == "Voz registrada com sucesso!"
    assert data["embedding"] == embedding_mock.tolist()
    
    # Verificar chamadas aos mocks
    mock_validar_token.assert_called_once_with("token_teste", "registrar_voz", mock_validar_token.call_args[0][2])
    mock_registrar_embedding.assert_called_once()

@patch('src.backend.api.endpoints_voz.validar_token_temporario')
def test_registrar_voz_sem_token(mock_validar_token, client):
    """Testa o registro de voz sem token de autorização."""
    # Preparar arquivo de áudio simulado
    test_file = io.BytesIO(b"test audio content")
    
    # Fazer requisição sem token
    response = client.post(
        "/api/registrar-voz",
        files={"arquivo": ("test.wav", test_file, "audio/wav")}
    )
    
    # Verificar resultado
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Token temporário ausente"
    
    # Verificar que o mock não foi chamado
    mock_validar_token.assert_not_called()

@patch('src.backend.api.endpoints_voz.validar_token_temporario')
def test_registrar_voz_token_invalido(mock_validar_token, client):
    """Testa o registro de voz com token inválido."""
    # Configurar mock para retornar None (token inválido)
    mock_validar_token.return_value = None
    
    # Preparar arquivo de áudio simulado
    test_file = io.BytesIO(b"test audio content")
    
    # Fazer requisição
    response = client.post(
        "/api/registrar-voz",
        files={"arquivo": ("test.wav", test_file, "audio/wav")},
        headers={"Authorization": "Bearer token_invalido"}
    )
    
    # Verificar resultado
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Token temporário inválido ou ação não permitida"
    
    # Verificar chamada ao mock
    mock_validar_token.assert_called_once()

@patch('src.backend.api.endpoints_voz.validar_token_temporario')
@patch('src.backend.api.endpoints_voz.registrar_embedding_voz')
def test_registrar_voz_erro_processamento(mock_registrar_embedding, mock_validar_token, client):
    """Testa o registro de voz com erro no processamento."""
    # Configurar mocks
    usuario_mock = MagicMock()
    usuario_mock.id = 1
    usuario_mock.email = "teste@example.com"
    mock_validar_token.return_value = usuario_mock
    
    # Simular erro no processamento
    mock_registrar_embedding.side_effect = Exception("Erro ao processar áudio")
    
    # Preparar arquivo de áudio simulado
    test_file = io.BytesIO(b"test audio content")
    
    # Fazer requisição
    response = client.post(
        "/api/registrar-voz",
        files={"arquivo": ("test.wav", test_file, "audio/wav")},
        headers={"Authorization": "Bearer token_teste"}
    )
    
    # Verificar resultado
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert "Erro ao registrar voz" in data["detail"]
    
    # Verificar chamadas aos mocks
    mock_validar_token.assert_called_once()
    mock_registrar_embedding.assert_called_once()

@patch('src.backend.api.endpoints_voz.validar_token_temporario')
@patch('src.backend.api.endpoints_voz.autenticar_por_voz')
@patch('src.backend.api.endpoints_voz.criar_token_acesso')
def test_autenticar_voz_sucesso(mock_criar_token, mock_autenticar, mock_validar_token, client):
    """Testa a autenticação por voz com sucesso."""
    # Configurar mocks
    usuario_mock = MagicMock()
    usuario_mock.id = 1
    usuario_mock.email = "teste@example.com"
    mock_validar_token.return_value = usuario_mock
    
    # Simular alta similaridade (autenticação bem-sucedida)
    mock_autenticar.return_value = 0.95
    mock_criar_token.return_value = "access_token_teste"
    
    # Preparar arquivo de áudio simulado
    test_file = io.BytesIO(b"test audio content")
    
    # Fazer requisição
    response = client.post(
        "/api/autenticar-voz",
        files={"arquivo": ("test.wav", test_file, "audio/wav")},
        headers={"Authorization": "Bearer token_teste"}
    )
    
    # Verificar resultado
    assert response.status_code == 200
    data = response.json()
    assert "mensagem" in data
    assert "pontuacao_similaridade" in data
    assert "access_token" in data
    assert data["mensagem"] == "Autenticação por voz bem-sucedida"
    assert data["pontuacao_similaridade"] == 95.0  # 0.95 * 100
    assert data["access_token"] == "access_token_teste"
    
    # Verificar chamadas aos mocks
    mock_validar_token.assert_called_once()
    mock_autenticar.assert_called_once()
    mock_criar_token.assert_called_once()

@patch('src.backend.api.endpoints_voz.validar_token_temporario')
@patch('src.backend.api.endpoints_voz.autenticar_por_voz')
def test_autenticar_voz_falha_similaridade(mock_autenticar, mock_validar_token, client):
    """Testa a autenticação por voz com baixa similaridade."""
    # Configurar mocks
    usuario_mock = MagicMock()
    usuario_mock.id = 1
    usuario_mock.email = "teste@example.com"
    mock_validar_token.return_value = usuario_mock
    
    # Simular baixa similaridade (autenticação falha)
    mock_autenticar.return_value = 0.5
    
    # Preparar arquivo de áudio simulado
    test_file = io.BytesIO(b"test audio content")
    
    # Fazer requisição
    response = client.post(
        "/api/autenticar-voz",
        files={"arquivo": ("test.wav", test_file, "audio/wav")},
        headers={"Authorization": "Bearer token_teste"}
    )
    
    # Verificar resultado
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert "mensagem" in data["detail"]
    assert "pontuacao_similaridade" in data["detail"]
    assert data["detail"]["mensagem"] == "Autenticação por voz falhou"
    assert data["detail"]["pontuacao_similaridade"] == 50.0  # 0.5 * 100
    
    # Verificar chamadas aos mocks
    mock_validar_token.assert_called_once()
    mock_autenticar.assert_called_once()

@patch('src.backend.api.endpoints_voz.validar_token_temporario')
def test_autenticar_voz_token_invalido(mock_validar_token, client):
    """Testa a autenticação por voz com token inválido."""
    # Configurar mock para retornar None (token inválido)
    mock_validar_token.return_value = None
    
    # Preparar arquivo de áudio simulado
    test_file = io.BytesIO(b"test audio content")
    
    # Fazer requisição
    response = client.post(
        "/api/autenticar-voz",
        files={"arquivo": ("test.wav", test_file, "audio/wav")},
        headers={"Authorization": "Bearer token_invalido"}
    )
    
    # Verificar resultado
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Token temporário inválido ou ação não permitida"
    
    # Verificar chamada ao mock
    mock_validar_token.assert_called_once()
