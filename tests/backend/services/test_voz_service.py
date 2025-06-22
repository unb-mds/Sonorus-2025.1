import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from src.backend.services import voz_service

# src/backend/services/test_voz_service.py

@pytest.fixture
def mock_upload_file():
    mock = MagicMock()
    mock.file = MagicMock()
    return mock

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def usuario():
    user = MagicMock()
    user.embedding = [0.1, 0.2, 0.3]
    user.cadastro_completo = False
    return user

def test_validar_e_normalizar_audio_sucesso_mono():
    dados = np.ones(16000, dtype=np.float32)
    with patch("src.backend.services.voz_service.sf.read", return_value=(dados, 16000)), \
         patch("src.backend.services.voz_service.sf.write") as mock_write:
        voz_service.validar_e_normalizar_audio("audio.wav")
        mock_write.assert_called_once()

def test_validar_e_normalizar_audio_sucesso_estereo():
    dados = np.ones((16000, 2), dtype=np.float32)
    with patch("src.backend.services.voz_service.sf.read", return_value=(dados, 16000)), \
         patch("src.backend.services.voz_service.sf.write") as mock_write, \
         patch("src.backend.services.voz_service.np.mean", side_effect=lambda x, axis: x[:,0]):
        voz_service.validar_e_normalizar_audio("audio.wav")
        mock_write.assert_called_once()

def test_validar_e_normalizar_audio_taxa_diferente():
    dados = np.ones(16000, dtype=np.float32)
    with patch("src.backend.services.voz_service.sf.read", return_value=(dados, 8000)), \
         patch("src.backend.services.voz_service.librosa.resample", return_value=dados), \
         patch("src.backend.services.voz_service.sf.write") as mock_write:
        voz_service.validar_e_normalizar_audio("audio.wav")
        mock_write.assert_called_once()

def test_validar_e_normalizar_audio_duracao_maior_que_30s():
    dados = np.ones(16001, dtype=np.float32)
    with patch("src.backend.services.voz_service.sf.read", return_value=(dados, 500)), \
         pytest.raises(ValueError):
        voz_service.validar_e_normalizar_audio("audio.wav")

@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.validar_e_normalizar_audio")
@patch("src.backend.services.voz_service.get_embedding")
@patch("src.backend.services.voz_service.redis_client")
@patch("src.backend.services.voz_service.os.remove")
def test_registrar_embedding_voz_sucesso(mock_remove, mock_redis, mock_get_embedding, mock_validar, mock_copy, mock_temp, mock_db, usuario, mock_upload_file):
    temp_file = MagicMock()
    temp_file.name = "temp.wav"
    mock_temp.return_value.__enter__.return_value = temp_file
    mock_get_embedding.return_value = np.array([0.1, 0.2, 0.3])
    mock_db.query().filter_by().first.return_value = usuario

    result = voz_service.registrar_embedding_voz(1, mock_upload_file, mock_db)
    assert np.allclose(result, [0.1, 0.2, 0.3])
    mock_redis.setex.assert_called()
    mock_db.commit.assert_called_once()
    mock_remove.assert_called_once_with("temp.wav")
    assert usuario.cadastro_completo is True

@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.validar_e_normalizar_audio")
@patch("src.backend.services.voz_service.get_embedding")
@patch("src.backend.services.voz_service.redis_client")
@patch("src.backend.services.voz_service.os.remove")
def test_registrar_embedding_voz_usuario_nao_encontrado(mock_remove, mock_redis, mock_get_embedding, mock_validar, mock_copy, mock_temp, mock_db, mock_upload_file):
    temp_file = MagicMock()
    temp_file.name = "temp.wav"
    mock_temp.return_value.__enter__.return_value = temp_file
    mock_db.query().filter_by().first.return_value = None

    with pytest.raises(HTTPException) as exc:
        voz_service.registrar_embedding_voz(1, mock_upload_file, mock_db)
    assert exc.value.status_code == 404
    mock_remove.assert_called_once_with("temp.wav")

@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.validar_e_normalizar_audio", side_effect=ValueError("erro"))
@patch("src.backend.services.voz_service.os.remove")
def test_registrar_embedding_voz_value_error(mock_remove, mock_validar, mock_copy, mock_temp, mock_db, mock_upload_file):
    temp_file = MagicMock()
    temp_file.name = "temp.wav"
    mock_temp.return_value.__enter__.return_value = temp_file

    with pytest.raises(ValueError):
        voz_service.registrar_embedding_voz(1, mock_upload_file, mock_db)
    mock_db.rollback.assert_called_once()
    mock_remove.assert_called_once_with("temp.wav")

@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.validar_e_normalizar_audio", side_effect=Exception("erro"))
@patch("src.backend.services.voz_service.os.remove")
def test_registrar_embedding_voz_erro_generico(mock_remove, mock_validar, mock_copy, mock_temp, mock_db, mock_upload_file):
    temp_file = MagicMock()
    temp_file.name = "temp.wav"
    mock_temp.return_value.__enter__.return_value = temp_file

    with pytest.raises(HTTPException) as exc:
        voz_service.registrar_embedding_voz(1, mock_upload_file, mock_db)
    assert exc.value.status_code == 500
    mock_db.rollback.assert_called_once()
    mock_remove.assert_called_once_with("temp.wav")

@patch("src.backend.services.voz_service.redis_client")
def test_get_embedding_usuario_cache_cache(mock_redis, mock_db):
    mock_redis.get.return_value = '[0.1, 0.2, 0.3]'
    result = voz_service.get_embedding_usuario_cache(1, mock_db)
    assert np.allclose(result, [0.1, 0.2, 0.3])

@patch("src.backend.services.voz_service.redis_client")
def test_get_embedding_usuario_cache_db(mock_redis, mock_db):
    mock_redis.get.return_value = None
    usuario = MagicMock()
    usuario.embedding = [0.1, 0.2, 0.3]
    mock_db.query().filter_by().first.return_value = usuario
    result = voz_service.get_embedding_usuario_cache(1, mock_db)
    assert np.allclose(result, [0.1, 0.2, 0.3])
    mock_redis.setex.assert_called()

@patch("src.backend.services.voz_service.redis_client")
def test_get_embedding_usuario_cache_none(mock_redis, mock_db):
    mock_redis.get.return_value = None
    mock_db.query().filter_by().first.return_value = None
    result = voz_service.get_embedding_usuario_cache(1, mock_db)
    assert result is None

@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.validar_e_normalizar_audio")
@patch("src.backend.services.voz_service.get_embedding_usuario_cache")
@patch("src.backend.services.voz_service.get_embedding")
@patch("src.backend.services.voz_service.comparar_embeddings")
@patch("src.backend.services.voz_service.os.remove")
def test_autenticar_por_voz_sucesso(mock_remove, mock_comparar, mock_get_embedding, mock_get_cache, mock_validar, mock_copy, mock_temp, mock_db, mock_upload_file):
    temp_file = MagicMock()
    temp_file.name = "temp.wav"
    mock_temp.return_value.__enter__.return_value = temp_file
    mock_get_cache.return_value = np.array([0.1, 0.2, 0.3])
    mock_get_embedding.return_value = np.array([0.1, 0.2, 0.3])
    mock_comparar.return_value = 0.99

    result = voz_service.autenticar_por_voz(1, mock_upload_file, mock_db)
    assert result == 0.99
    mock_remove.assert_called_once_with("temp.wav")

@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.validar_e_normalizar_audio")
@patch("src.backend.services.voz_service.get_embedding_usuario_cache", return_value=None)
@patch("src.backend.services.voz_service.os.remove")
def test_autenticar_por_voz_embedding_nao_encontrado(mock_remove, mock_get_cache, mock_validar, mock_copy, mock_temp, mock_db, mock_upload_file):
    temp_file = MagicMock()
    temp_file.name = "temp.wav"
    mock_temp.return_value.__enter__.return_value = temp_file

    with pytest.raises(HTTPException) as exc:
        voz_service.autenticar_por_voz(1, mock_upload_file, mock_db)
    assert exc.value.status_code == 404
    mock_remove.assert_called_once_with("temp.wav")

@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.validar_e_normalizar_audio", side_effect=Exception("erro"))
@patch("src.backend.services.voz_service.os.remove")
def test_autenticar_por_voz_erro_generico(mock_remove, mock_validar, mock_copy, mock_temp, mock_db, mock_upload_file):
    temp_file = MagicMock()
    temp_file.name = "temp.wav"
    mock_temp.return_value.__enter__.return_value = temp_file

    with pytest.raises(HTTPException) as exc:
        voz_service.autenticar_por_voz(1, mock_upload_file, mock_db)
    assert exc.value.status_code == 500
    mock_remove.assert_called_once_with("temp.wav")