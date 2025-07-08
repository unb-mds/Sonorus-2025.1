import json
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException, Request
from src.backend.models.modelos import UsuarioRegistro
from src.backend.api import autenticacao

@patch('src.backend.api.autenticacao.dominio_tem_mx')
@patch('src.backend.api.autenticacao.criar_token_temporario')
def test_registrar_sucesso(mock_criar_token, mock_dominio_mx, client, mock_db):
    mock_dominio_mx.return_value = True
    mock_criar_token.return_value = "token_temporario_teste"
    mock_db.query().filter_by().first.side_effect = [None, None]

    usuario_teste = {
        "nome": "Teste",
        "sobrenome": "Usuário",
        "email": "teste@example.com",
        "senha": "senha123"
    }

    response = client.post("/api/registrar", json=usuario_teste)

    assert response.status_code == 200
    data = response.json()
    assert "mensagem" in data
    assert data["mensagem"].startswith("Usuário registrado")
    mock_dominio_mx.assert_called_once_with("example.com")
    mock_criar_token.assert_called_once()

def test_registrar_usuario_existente(client, mock_db):
    """Testa o registro de um usuário que já existe."""
    usuario_mock = MagicMock()
    mock_db.query().filter_by().first.side_effect = [usuario_mock]  # Usuário já existe

    usuario_teste = {
        "nome": "Teste",
        "sobrenome": "Existente",
        "email": "existente@example.com",
        "senha": "senha123"
    }

    response = client.post("/api/registrar", json=usuario_teste)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Usuário já existe"

@patch('src.backend.api.autenticacao.dominio_tem_mx')
def test_registrar_dominio_invalido(mock_dominio_mx, client, mock_db):
    """Testa o registro com um domínio de email inválido."""
    mock_dominio_mx.return_value = False
    mock_db.query().filter_by().first.side_effect = [None, None]

    usuario_teste = {
        "nome": "Teste",
        "sobrenome": "Domínio",
        "email": "teste@dominioinvalido.com",
        "senha": "senha123"
    }

    response = client.post("/api/registrar", json=usuario_teste)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Domínio de e-mail inexistente ou inválido"
    mock_dominio_mx.assert_called_once_with("dominioinvalido.com")

@patch('src.backend.api.autenticacao.autenticar_usuario')
@patch('src.backend.api.autenticacao.criar_token_temporario')
def test_login_sucesso(mock_criar_token, mock_autenticar, client, mock_db):
    """Testa o login com credenciais válidas."""
    usuario_mock = MagicMock()
    usuario_mock.cadastro_completo = True
    mock_db.query().filter_by().first.return_value = usuario_mock
    mock_autenticar.return_value = True
    mock_criar_token.return_value = "token_temporario_teste"

    form_data = {
        "email": "usuario@example.com",
        "password": "senha123"
    }

    response = client.post("/api/login", data=form_data)

    assert response.status_code == 200
    data = response.json()
    assert "mensagem" in data
    assert "pre_auth_token" in data
    assert data["pre_auth_token"] == "token_temporario_teste"

@patch('src.backend.api.autenticacao.autenticar_usuario')
def test_login_credenciais_invalidas(mock_autenticar, client, mock_db):
    """Testa o login com credenciais inválidas."""
    mock_db.query().filter_by().first.return_value = None
    mock_autenticar.return_value = False

    form_data = {
        "email": "usuario@example.com",
        "password": "senha_errada"
    }

    response = client.post("/api/login", data=form_data)

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "E-mail ou senha inválidos"

@patch('src.backend.api.autenticacao.dominio_tem_mx')
def test_check_email_valido(mock_dominio_mx, client, mock_db):
    """Testa a verificação de email válido e disponível."""
    mock_dominio_mx.return_value = True
    mock_db.query().filter().first.return_value = None

    email_teste = {"email": "novo@example.com"}

    response = client.post("/api/check-email", json=email_teste)

    assert response.status_code == 200
    data = response.json()
    assert data["mensagem"] == "E-mail válido e disponível"
    mock_dominio_mx.assert_called_once_with("example.com")

@patch('src.backend.api.autenticacao.dominio_tem_mx')
def test_check_email_invalido(mock_dominio_mx, client, mock_db):
    """Testa a verificação de email com domínio inválido."""
    mock_dominio_mx.return_value = False
    mock_db.query().filter().first.return_value = None

    email_teste = {"email": "teste@dominioinvalido.com"}

    response = client.post("/api/check-email", json=email_teste)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Domínio de e-mail inválido"
    mock_dominio_mx.assert_called_once_with("dominioinvalido.com")

def test_check_email_ja_cadastrado(client, mock_db):
    """Testa a verificação de email já cadastrado."""
    usuario_mock = MagicMock()
    mock_db.query().filter().first.return_value = usuario_mock

    email_teste = {"email": "existente@example.com"}

    response = client.post("/api/check-email", json=email_teste)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "E-mail já cadastrado no sistema"

@patch('src.backend.api.autenticacao.dominio_tem_mx')
def test_registrar_email_invalido(mock_dominio_mx, client, mock_db):
    """Testa o registro com email mal formatado."""
    mock_dominio_mx.return_value = True
    mock_db.query().filter_by().first.side_effect = [None, None]

    usuario_teste = {
        "nome": "Teste",
        "sobrenome": "Usuario",
        "email": "emailinvalido",
        "senha": "senha123"
    }

    response = client.post("/api/registrar", json=usuario_teste)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Formato de e-mail inválido"

def test_registrar_remove_incompleto(client, mock_db):
    """Testa se usuário incompleto é removido antes de novo registro."""
    usuario_incompleto = MagicMock()
    mock_db.query().filter_by().first.side_effect = [None, usuario_incompleto]
    with patch('src.backend.api.autenticacao.dominio_tem_mx', return_value=True), \
         patch('src.backend.api.autenticacao.criar_token_temporario', return_value="token"):
        usuario_teste = {
            "nome": "Novo",
            "sobrenome": "Usuario",
            "email": "novo@exemplo.com",
            "senha": "senha123"
        }
        response = client.post("/api/registrar", json=usuario_teste)
        assert response.status_code == 200
        # O delete e commit devem ser chamados para remover o incompleto
        assert mock_db.delete.called
        assert mock_db.commit.called

@patch('src.backend.api.autenticacao.autenticar_usuario')
def test_login_cadastro_incompleto(mock_autenticar, client, mock_db):
    """Testa login quando cadastro não está completo."""
    usuario_mock = MagicMock()
    usuario_mock.cadastro_completo = False
    mock_db.query().filter_by().first.return_value = usuario_mock
    mock_autenticar.return_value = True

    form_data = {
        "email": "usuario@incompleto.com",
        "password": "senha123"
    }

    response = client.post("/api/login", data=form_data)
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Finalize o cadastro de voz para acessar o sistema"

def test_login_formato_incorreto(client, mock_db):
    """Testa login sem enviar campos obrigatórios."""
    response = client.post("/api/login", data={})
    assert response.status_code == 422

def test_check_email_formato_invalido(client, mock_db):
    """Testa check-email com email mal formatado."""
    mock_db.query().filter().first.return_value = None
    email_teste = {"email": "emailinvalido"}
    response = client.post("/api/check-email", json=email_teste)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Formato de e-mail inválido"

def test_get_jwt_from_cookie_sucesso():
    """Testa extração de token do cookie."""
    class DummyRequest:
        cookies = {"access_token": "meutoken"}
    assert autenticacao.get_jwt_from_cookie(DummyRequest()) == "meutoken"

def test_get_jwt_from_cookie_falha():
    """Testa erro ao não encontrar token no cookie."""
    class DummyRequest:
        cookies = {}
    with pytest.raises(HTTPException) as exc:
        autenticacao.get_jwt_from_cookie(DummyRequest())
    assert exc.value.status_code == 401
    assert exc.value.detail == "Token não encontrado"

def test_rota_protegida_sucesso():
    """Testa acesso à rota protegida."""
    resp = autenticacao.rota_protegida(token="abc")
    assert resp["mensagem"] == "Acesso autorizado!"

@patch('dns.resolver.resolve')
def test_dominio_tem_mx_true(mock_resolve):
    """Testa domínio com MX válido."""
    mock_resolve.return_value = [MagicMock()]
    assert autenticacao.dominio_tem_mx("gmail.com") is True

@patch('dns.resolver.resolve', side_effect=Exception("fail"))
def test_dominio_tem_mx_false(mock_resolve):
    """Testa domínio sem MX."""
    assert autenticacao.dominio_tem_mx("dominioinvalido.com") is False
