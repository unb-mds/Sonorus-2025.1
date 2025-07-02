import pytest
from fastapi.testclient import TestClient
from src.backend.main import app, get_db
from sqlalchemy.orm import Session

def test_routers_registered():
    routes = [route.path for route in app.routes]
    # Verifica se as rotas principais dos roteadores estão presentes
    assert "/api/registrar" in routes or "/api/login" in routes  # autenticacao
    assert "/api/registrar-voz" in routes or "/api/autenticar-voz" in routes  # voz
    assert "/api/test-db" in routes  # banco

def test_cors_middleware_present():
    middlewares = [mw.cls.__name__ for mw in app.user_middleware]
    assert "CORSMiddleware" in middlewares

def test_get_db_returns_session():
    # Testa se get_db retorna um Session e fecha corretamente
    gen = get_db()
    db = next(gen)
    assert isinstance(db, Session)
    # Finaliza o generator para fechar a conexão
    try:
        next(gen)
    except StopIteration:
        pass