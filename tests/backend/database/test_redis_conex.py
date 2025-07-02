from unittest.mock import patch, MagicMock
import src.backend.database.redis_conex as redis_conex

def test_redis_client_config():
    # Verifica se as variáveis de ambiente foram lidas corretamente
    assert redis_conex.REDIS_HOST is not None
    assert isinstance(redis_conex.REDIS_PORT, int)
    assert isinstance(redis_conex.REDIS_DB, int)

@patch("src.backend.database.redis_conex.redis.Redis")
def test_redis_client_instantiation(mock_redis):
    # Força o Redis a retornar um mock
    mock_instance = MagicMock()
    mock_redis.return_value = mock_instance

    # Reimporta o módulo para executar a criação do cliente com o mock
    import importlib
    importlib.reload(redis_conex)

    mock_redis.assert_called_once_with(
        host=redis_conex.REDIS_HOST,
        port=redis_conex.REDIS_PORT,
        db=redis_conex.REDIS_DB,
        password=redis_conex.REDIS_PASSWORD,
        decode_responses=True
    )