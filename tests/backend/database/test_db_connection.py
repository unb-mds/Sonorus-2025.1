import pytest
from src.backend.database import db_connection

def test_engine_and_sessionlocal_exist():
    assert db_connection.engine is not None
    assert db_connection.SessionLocal is not None

def test_base_is_declarative_base():
    assert hasattr(db_connection.Base, "metadata")

def test_get_db_yields_and_closes():
    # Mock SessionLocal para não conectar ao banco real
    class DummySession:
        closed = False
        def close(self):
            self.closed = True

    original_sessionlocal = db_connection.SessionLocal
    db_connection.SessionLocal = lambda: DummySession()
    gen = db_connection.get_db()
    db = next(gen)
    assert isinstance(db, DummySession)
    # Finaliza o generator para chamar close
    try:
        next(gen)
    except StopIteration:
        pass
    assert db.closed is True
    db_connection.SessionLocal = original_sessionlocal