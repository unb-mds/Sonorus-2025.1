import pytest
from src.backend.models.sqlalchemy import Usuario

def test_usuario_criacao():
    usuario = Usuario(
        id=1,
        nome="Maria",
        sobrenome="Oliveira",
        email="maria@exemplo.com",
        senha="hashsenha",
        embedding=[0.1, 0.2, 0.3],
        cadastro_completo=True
    )
    assert usuario.id == 1
    assert usuario.nome == "Maria"
    assert usuario.sobrenome == "Oliveira"
    assert usuario.email == "maria@exemplo.com"
    assert usuario.senha == "hashsenha"
    assert usuario.embedding == [0.1, 0.2, 0.3]
    assert usuario.cadastro_completo is True

def test_usuario_repr():
    usuario = Usuario(
        nome="Ana",
        sobrenome="Silva",
        email="ana@exemplo.com",
        senha="hash",
    )
    repr_str = repr(usuario)
    assert "Ana" in repr_str
    assert "Silva" in repr_str
    assert "ana@exemplo.com" in repr_str