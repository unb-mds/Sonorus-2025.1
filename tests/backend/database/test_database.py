from src.backend.database import database

def test_usuarios_db_dict():
    # O dicionário deve estar disponível e ser mutável
    database.usuarios_db.clear()
    database.usuarios_db["teste"] = {"nome": "João"}
    assert "teste" in database.usuarios_db
    assert database.usuarios_db["teste"]["nome"] == "João"

def test_initialize_db(capsys):
    database.initialize_db()
    captured = capsys.readouterr()
    assert "Banco de dados simulado inicializado" in captured.out