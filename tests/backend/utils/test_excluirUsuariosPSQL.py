# filepath: tests/backend/utils/test_excluirUsuariosPSQL.py
import pytest
from unittest.mock import MagicMock, patch

@patch("src.backend.utils.excluirUsuariosPSQL.SessionLocal")
@patch("src.backend.utils.excluirUsuariosPSQL.Usuario")
def test_excluir_usuarios_sucesso(MockUsuario, MockSessionLocal, capsys):
    # Mock da sessão e query
    mock_session = MagicMock()
    MockSessionLocal.return_value = mock_session
    mock_query = mock_session.query.return_value
    mock_query.delete.return_value = 42  # Simula 42 usuários deletados

    # Executa o script
    from src.backend.utils.excluirUsuariosPSQL import excluir_todos_usuarios
    excluir_todos_usuarios()

    # Verifica se os métodos foram chamados
    mock_session.query.assert_called_once_with(MockUsuario)
    mock_query.delete.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()

    # Verifica saída do print
    captured = capsys.readouterr()
    assert "Todos os usuários foram removidos." in captured.out

@patch("src.backend.utils.excluirUsuariosPSQL.SessionLocal")
@patch("src.backend.utils.excluirUsuariosPSQL.Usuario")
def test_excluir_usuarios_falha(MockUsuario, MockSessionLocal, capsys):
    # Mock da sessão e query
    mock_session = MagicMock()
    MockSessionLocal.return_value = mock_session
    mock_query = mock_session.query.return_value
    # Simula erro ao deletar
    mock_query.delete.side_effect = Exception("Erro ao deletar usuários")

    # Executa o script e espera exceção
    from src.backend.utils.excluirUsuariosPSQL import excluir_todos_usuarios
    with pytest.raises(Exception, match="Erro ao deletar usuários"):
        excluir_todos_usuarios()

    # Verifica se close foi chamado mesmo com erro
    mock_session.close.assert_called_once()