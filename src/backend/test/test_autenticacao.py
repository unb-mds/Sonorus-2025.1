import json
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.backend.models.modelos import UsuarioRegistro

@patch('src.backend.api.autenticacao.registrar_usuario')
@patch('src.backend.api.autenticacao.dominio_tem_mx')
@patch('src.backend.api.autenticacao.criar_token_temporario')
def test_registrar_sucesso(mock_criar_token, mock_dominio_mx, mock_registrar, client):
    """Testa o registro de usuário com sucesso."""
    # Configurar mocks
    mock_registrar.return_value = True
    mock_dominio_mx.return_value = True
    mock_criar_token.return_value = "token_temporario_teste"
    
    # Dados de teste
    usuario_teste = {
        "nome": "Teste",
        "sobrenome": "Usuário",
        "email": "teste@example.com",
        "senha": "senha123"
    }
    
    # Fazer requisição
    response = client.post("/registrar", json=usuario_teste)
    
    # Verificar resultado
    assert response.status_code == 200
    data = response.json()
    assert "mensagem" in data
    assert "pre_auth_token" in data
    assert data["pre_auth_token"] == "token_temporario_teste"
    
    # Verificar chamadas aos mocks
    mock_registrar.assert_called_once()
    mock_dominio_mx.assert_called_once_with("example.com")
    mock_criar_token.assert_called_once()

@patch('src.backend.api.autenticacao.registrar_usuario')
def test_registrar_usuario_existente(mock_registrar, client):
    """Testa o registro de um usuário que já existe."""
    # Configurar mock para simular usuário já existente
    mock_registrar.return_value = False
    
    # Dados de teste
    usuario_teste = {
        "nome": "Teste",
        "sobrenome": "Existente",
        "email": "existente@example.com",
        "senha": "senha123"
    }
    
    # Fazer requisição
    response = client.post("/registrar", json=usuario_teste)
    
    # Verificar resultado
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Usuário já existe"
    
    # Verificar chamada ao mock
    mock_registrar.assert_called_once()

@patch('src.backend.api.autenticacao.dominio_tem_mx')
@patch('src.backend.api.autenticacao.registrar_usuario')
def test_registrar_dominio_invalido(mock_registrar, mock_dominio_mx, client):
    """Testa o registro com um domínio de email inválido."""
    # Configurar mocks
    mock_registrar.return_value = True
    mock_dominio_mx.return_value = False
    
    # Dados de teste
    usuario_teste = {
        "nome": "Teste",
        "sobrenome": "Domínio",
        "email": "teste@dominioinvalido.com",
        "senha": "senha123"
    }
    
    # Fazer requisição
    response = client.post("/registrar", json=usuario_teste)
    
    # Verificar resultado
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Domínio de e-mail inexistente ou inválido"
    
    # Verificar chamadas aos mocks
    mock_registrar.assert_called_once()
    mock_dominio_mx.assert_called_once_with("dominioinvalido.com")

@patch('src.backend.api.autenticacao.autenticar_usuario')
@patch('src.backend.api.autenticacao.criar_token_temporario')
def test_login_sucesso(mock_criar_token, mock_autenticar, client):
    """Testa o login com credenciais válidas."""
    # Configurar mocks
    mock_autenticar.return_value = True
    mock_criar_token.return_value = "token_temporario_teste"
    
    # Dados de teste
    form_data = {
        "email": "usuario@example.com",
        "password": "senha123"
    }
    
    # Fazer requisição
    response = client.post("/login", data=form_data)
    
    # Verificar resultado
    assert response.status_code == 200
    data = response.json()
    assert "mensagem" in data
    assert "pre_auth_token" in data
    assert data["pre_auth_token"] == "token_temporario_teste"
    
    # Verificar chamadas aos mocks
    mock_autenticar.assert_called_once_with("usuario@example.com", "senha123", mock_autenticar.call_args[0][2])
    mock_criar_token.assert_called_once()

@patch('src.backend.api.autenticacao.autenticar_usuario')
def test_login_credenciais_invalidas(mock_autenticar, client):
    """Testa o login com credenciais inválidas."""
    # Configurar mock para simular falha na autenticação
    mock_autenticar.return_value = False
    
    # Dados de teste
    form_data = {
        "email": "usuario@example.com",
        "password": "senha_errada"
    }
    
    # Fazer requisição
    response = client.post("/login", data=form_data)
    
    # Verificar resultado
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "E-mail ou senha inválidos"
    
    # Verificar chamada ao mock
    mock_autenticar.assert_called_once()

@patch('src.backend.api.autenticacao.dominio_tem_mx')
def test_check_email_valido(mock_dominio_mx, client, mock_db):
    """Testa a verificação de email válido e disponível."""
    # Configurar mock
    mock_dominio_mx.return_value = True
    mock_db.query().filter().first.return_value = None
    
    # Dados de teste
    email_teste = {"email": "novo@example.com"}
    
    # Fazer requisição com mock do banco de dados
    with patch('src.backend.api.autenticacao.get_db', return_value=mock_db):
        response = client.post("/check-email", json=email_teste)
    
    # Verificar resultado
    assert response.status_code == 200
    data = response.json()
    assert "mensagem" in data
    assert data["mensagem"] == "E-mail válido e disponível"
    
    # Verificar chamada ao mock
    mock_dominio_mx.assert_called_once_with("example.com")

@patch('src.backend.api.autenticacao.dominio_tem_mx')
def test_check_email_invalido(mock_dominio_mx, client, mock_db):
    """Testa a verificação de email com domínio inválido."""
    # Configurar mock
    mock_dominio_mx.return_value = False
    mock_db.query().filter().first.return_value = None
    
    # Dados de teste
    email_teste = {"email": "teste@dominioinvalido.com"}
    
    # Fazer requisição com mock do banco de dados
    with patch('src.backend.api.autenticacao.get_db', return_value=mock_db):
        response = client.post("/check-email", json=email_teste)
    
    # Verificar resultado
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Domínio de e-mail inválido"
    
    # Verificar chamada ao mock
    mock_dominio_mx.assert_called_once_with("dominioinvalido.com")

def test_check_email_ja_cadastrado(client, mock_db):
    """Testa a verificação de email já cadastrado."""
    # Configurar mock para simular email já cadastrado
    usuario_mock = MagicMock()
    mock_db.query().filter().first.return_value = usuario_mock
    
    # Dados de teste
    email_teste = {"email": "existente@example.com"}
    
    # Fazer requisição com mock do banco de dados
    with patch('src.backend.api.autenticacao.get_db', return_value=mock_db):
        response = client.post("/check-email", json=email_teste)
    
    # Verificar resultado
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "E-mail já cadastrado no sistema"
