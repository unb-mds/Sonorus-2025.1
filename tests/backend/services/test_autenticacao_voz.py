import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from src.backend.services import autenticacao_voz

# src/backend/services/test_autenticacao_voz.py

@pytest.fixture
def mock_arquivo():
    mock = MagicMock()
    mock.file = MagicMock()
    return mock

def test_processar_e_verificar_voz_sucesso(mock_arquivo):
    login = "lemes"
    dados_audio = MagicMock()
    taxa_amostragem = 16000
    pontuacao = 0.95
    caminho_temp = autenticacao_voz.os.path.join(autenticacao_voz.AUDIOS_DIR, f"temp_{login}.wav")

    with patch("src.backend.services.autenticacao_voz.sf.read", return_value=(dados_audio, taxa_amostragem)) as mock_read, \
         patch("src.backend.services.autenticacao_voz.sf.write") as mock_write, \
         patch("src.backend.services.autenticacao_voz.modelo_ecapa.verificar_falante", return_value=pontuacao) as mock_verificar, \
         patch("src.backend.services.autenticacao_voz.os.path.exists", return_value=True) as mock_exists, \
         patch("src.backend.services.autenticacao_voz.os.remove") as mock_remove:
        resultado = autenticacao_voz.processar_e_verificar_voz(login, mock_arquivo)
        assert resultado == pontuacao
        mock_read.assert_called_once()
        mock_write.assert_called_once_with(caminho_temp, dados_audio, taxa_amostragem)
        mock_verificar.assert_called_once_with(caminho_temp, autenticacao_voz.embeddings_usuarios[login])
        mock_remove.assert_called_once_with(caminho_temp)

def test_processar_e_verificar_voz_usuario_nao_encontrado(mock_arquivo):
    login = "nao_existe"
    with pytest.raises(HTTPException) as exc:
        autenticacao_voz.processar_e_verificar_voz(login, mock_arquivo)
    assert exc.value.status_code == 404
    assert "Usuário não encontrado" in str(exc.value.detail)

def test_processar_e_verificar_voz_erro_interno(mock_arquivo):
    login = "lemes"
    caminho_temp = autenticacao_voz.os.path.join(autenticacao_voz.AUDIOS_DIR, f"temp_{login}.wav")
    with patch("src.backend.services.autenticacao_voz.sf.read", side_effect=Exception("erro")), \
         patch("src.backend.services.autenticacao_voz.os.path.exists", return_value=True) as mock_exists, \
         patch("src.backend.services.autenticacao_voz.os.remove") as mock_remove:
        with pytest.raises(HTTPException) as exc:
            autenticacao_voz.processar_e_verificar_voz(login, mock_arquivo)
        assert exc.value.status_code == 500
        assert "Erro interno no servidor" in str(exc.value.detail)
        mock_remove.assert_called_once_with(caminho_temp)

def test_processar_e_verificar_voz_finally_sem_arquivo(mock_arquivo):
    login = "lemes"
    with patch("src.backend.services.autenticacao_voz.sf.read", side_effect=Exception("erro")), \
         patch("src.backend.services.autenticacao_voz.os.path.exists", return_value=False) as mock_exists, \
         patch("src.backend.services.autenticacao_voz.os.remove") as mock_remove:
        with pytest.raises(HTTPException):
            autenticacao_voz.processar_e_verificar_voz(login, mock_arquivo)
        mock_remove.assert_not_called()