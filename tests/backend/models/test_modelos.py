import pytest
from pydantic import ValidationError
from src.backend.models.modelos import UsuarioRegistro, UsuarioLogin

def test_usuario_registro_sucesso():
    user = UsuarioRegistro(
        nome="João",
        sobrenome="Silva",
        email="joao@exemplo.com",
        senha="senha123"
    )
    assert user.nome == "João"
    assert user.sobrenome == "Silva"
    assert user.email == "joao@exemplo.com"
    assert user.senha == "senha123"

def test_usuario_registro_falha_campo_faltando():
    with pytest.raises(ValidationError):
        UsuarioRegistro(
            nome="João",
            sobrenome="Silva",
            email="joao@exemplo.com"
            # senha faltando
        )

def test_usuario_login_sucesso():
    login = UsuarioLogin(
        email="joao@exemplo.com",
        senha="senha123"
    )
    assert login.email == "joao@exemplo.com"
    assert login.senha == "senha123"

def test_usuario_login_falha_campo_faltando():
    with pytest.raises(ValidationError):
        UsuarioLogin(
            email="joao@exemplo.com"
            # senha faltando
        )