import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from src.backend.services import business_logic

# src/backend/services/test_business_logic.py


@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def usuario_registro():
    return MagicMock(nome="Nome", sobrenome="Sobrenome", email="email@teste.com", senha="senha123")

@pytest.fixture
def usuario_model():
    usuario = MagicMock()
    usuario.nome = "Nome"
    usuario.sobrenome = "Sobrenome"
    usuario.email = "email@teste.com"
    usuario.senha = business_logic.pwd_context.hash("senha123")
    usuario.embedding = [0.0]
    return usuario

def test_registrar_usuario_sucesso(mock_db, usuario_registro, usuario_model):
    mock_db.query().filter_by().first.return_value = None
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
    result = business_logic.registrar_usuario(usuario_registro, mock_db)
    assert result is True
    mock_db.add.assert_called()
    mock_db.commit.assert_called()
    mock_db.refresh.assert_called()

def test_registrar_usuario_email_existente(mock_db, usuario_registro, usuario_model):
    mock_db.query().filter_by().first.return_value = usuario_model
    result = business_logic.registrar_usuario(usuario_registro, mock_db)
    assert result is False

def test_autenticar_usuario_sucesso(mock_db, usuario_model):
    mock_db.query().filter_by().first.return_value = usuario_model
    result = business_logic.autenticar_usuario(usuario_model.email, "senha123", mock_db)
    assert result is True

def test_autenticar_usuario_usuario_nao_existe(mock_db):
    mock_db.query().filter_by().first.return_value = None
    result = business_logic.autenticar_usuario("email@teste.com", "senha123", mock_db)
    assert result is False

def test_autenticar_usuario_senha_incorreta(mock_db, usuario_model):
    usuario_model.senha = business_logic.pwd_context.hash("outra_senha")
    mock_db.query().filter_by().first.return_value = usuario_model
    result = business_logic.autenticar_usuario(usuario_model.email, "senha123", mock_db)
    assert result is False

def test_criar_token_acesso():
    dados = {"sub": "email@teste.com"}
    token = business_logic.criar_token_acesso(dados)
    assert isinstance(token, str)
    assert token.count('.') == 2  # JWT tem 3 partes

def test_criar_token_temporario():
    dados = {"sub": "email@teste.com", "acao": "registrar"}
    token = business_logic.criar_token_temporario(dados, minutos_expiracao=1)
    assert isinstance(token, str)
    assert token.count('.') == 2

@patch("src.backend.services.business_logic.jwt")
def test_obter_usuario_atual_sucesso(mock_jwt, mock_db, usuario_model):
    token = "token"
    mock_jwt.decode.return_value = {"sub": usuario_model.email}
    mock_db.query().filter_by().first.return_value = usuario_model
    result = business_logic.obter_usuario_atual(token, mock_db)
    assert result == usuario_model

@patch("src.backend.services.business_logic.jwt")
def test_obter_usuario_atual_token_invalido(mock_jwt, mock_db):
    token = "token"
    mock_jwt.decode.side_effect = business_logic.JWTError()
    with pytest.raises(HTTPException) as exc:
        business_logic.obter_usuario_atual(token, mock_db)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED

@patch("src.backend.services.business_logic.jwt")
def test_obter_usuario_atual_payload_sem_sub(mock_jwt, mock_db):
    token = "token"
    mock_jwt.decode.return_value = {}
    with pytest.raises(HTTPException) as exc:
        business_logic.obter_usuario_atual(token, mock_db)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED

@patch("src.backend.services.business_logic.jwt")
def test_obter_usuario_atual_usuario_nao_existe(mock_jwt, mock_db):
    token = "token"
    mock_jwt.decode.return_value = {"sub": "email@teste.com"}
    mock_db.query().filter_by().first.return_value = None
    with pytest.raises(HTTPException) as exc:
        business_logic.obter_usuario_atual(token, mock_db)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED

@patch("src.backend.services.business_logic.jwt")
def test_validar_token_temporario_sucesso(mock_jwt, mock_db, usuario_model):
    token = "token"
    mock_jwt.decode.return_value = {"sub": usuario_model.email, "acao": "registrar"}
    mock_db.query().filter_by().first.return_value = usuario_model
    result = business_logic.validar_token_temporario(token, "registrar", mock_db)
    assert result == usuario_model

@patch("src.backend.services.business_logic.jwt")
def test_validar_token_temporario_acao_errada(mock_jwt, mock_db, usuario_model):
    token = "token"
    mock_jwt.decode.return_value = {"sub": usuario_model.email, "acao": "outra_acao"}
    result = business_logic.validar_token_temporario(token, "registrar", mock_db)
    assert result is None

@patch("src.backend.services.business_logic.jwt")
def test_validar_token_temporario_usuario_nao_existe(mock_jwt, mock_db):
    token = "token"
    mock_jwt.decode.return_value = {"sub": "email@teste.com", "acao": "registrar"}
    mock_db.query().filter_by().first.return_value = None
    result = business_logic.validar_token_temporario(token, "registrar", mock_db)
    assert result is None

@patch("src.backend.services.business_logic.jwt")
def test_validar_token_temporario_payload_sem_sub(mock_jwt, mock_db):
    token = "token"
    mock_jwt.decode.return_value = {"acao": "registrar"}
    result = business_logic.validar_token_temporario(token, "registrar", mock_db)
    assert result is None

@patch("src.backend.services.business_logic.jwt")
def test_validar_token_temporario_jwt_error(mock_jwt, mock_db):
    token = "token"
    mock_jwt.decode.side_effect = business_logic.JWTError()
    result = business_logic.validar_token_temporario(token, "registrar", mock_db)
    assert result is None

def test_hash_senha():
    senha = "senha123"
    hash_result = business_logic.hash_senha(senha)
    assert business_logic.pwd_context.verify(senha, hash_result)