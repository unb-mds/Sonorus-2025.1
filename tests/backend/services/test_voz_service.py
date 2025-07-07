import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from src.backend.services import voz_service

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

# --- Testes para tratar_audio (antigo validar_e_normalizar_audio) ---

def test_tratar_audio_sucesso_mono():
    dados = np.ones(16000, dtype=np.float32)
    with patch("src.backend.services.voz_service.sf.read", return_value=(dados, 16000)), \
         patch("src.backend.services.voz_service.sf.write") as mock_write, \
         patch("src.backend.services.voz_service.bandpass_filter", return_value=dados), \
         patch("src.backend.services.voz_service.notch_filter", return_value=dados), \
         patch("src.backend.services.voz_service.apply_vad", return_value=dados), \
         patch("src.backend.services.voz_service.spectral_gate", return_value=dados):
        voz_service.tratar_audio("audio.wav")
        mock_write.assert_called_once()

def test_tratar_audio_sucesso_estereo():
    dados = np.ones((16000, 2), dtype=np.float32)
    with patch("src.backend.services.voz_service.sf.read", return_value=(dados, 16000)), \
         patch("src.backend.services.voz_service.sf.write") as mock_write, \
         patch("src.backend.services.voz_service.bandpass_filter", return_value=dados[:,0]), \
         patch("src.backend.services.voz_service.notch_filter", return_value=dados[:,0]), \
         patch("src.backend.services.voz_service.apply_vad", return_value=dados[:,0]), \
         patch("src.backend.services.voz_service.spectral_gate", return_value=dados[:,0]), \
         patch("src.backend.services.voz_service.np.mean", side_effect=lambda x, axis: x[:,0]):
        voz_service.tratar_audio("audio.wav")
        mock_write.assert_called_once()

def test_tratar_audio_taxa_diferente():
    dados = np.ones(16000, dtype=np.float32)
    with patch("src.backend.services.voz_service.sf.read", return_value=(dados, 8000)), \
         patch("src.backend.services.voz_service.librosa.resample", return_value=dados), \
         patch("src.backend.services.voz_service.sf.write") as mock_write, \
         patch("src.backend.services.voz_service.bandpass_filter", return_value=dados), \
         patch("src.backend.services.voz_service.notch_filter", return_value=dados), \
         patch("src.backend.services.voz_service.apply_vad", return_value=dados), \
         patch("src.backend.services.voz_service.spectral_gate", return_value=dados):
        voz_service.tratar_audio("audio.wav")
        mock_write.assert_called_once()

def test_tratar_audio_duracao_maior_que_30s():
    dados = np.ones(16001, dtype=np.float32)
    with patch("src.backend.services.voz_service.sf.read", return_value=(dados, 500)):
        with pytest.raises(ValueError):
            voz_service.tratar_audio("audio.wav")

def test_tratar_audio_convertido_para_int16():
    dados = np.ones(16000, dtype=np.float32) * 0.5
    with patch("src.backend.services.voz_service.sf.read", return_value=(dados, 16000)), \
         patch("src.backend.services.voz_service.sf.write") as mock_write, \
         patch("src.backend.services.voz_service.bandpass_filter", return_value=dados), \
         patch("src.backend.services.voz_service.notch_filter", return_value=dados), \
         patch("src.backend.services.voz_service.apply_vad", return_value=dados), \
         patch("src.backend.services.voz_service.spectral_gate", return_value=dados):
        voz_service.tratar_audio("audio.wav")
        mock_write.assert_called_once()

def test_tratar_audio_dtype_already_int16():
    dados = (np.ones(16000) * 1000).astype(np.int16)
    with patch("src.backend.services.voz_service.sf.read", return_value=(dados, 16000)), \
         patch("src.backend.services.voz_service.sf.write") as mock_write, \
         patch("src.backend.services.voz_service.bandpass_filter", return_value=dados), \
         patch("src.backend.services.voz_service.notch_filter", return_value=dados), \
         patch("src.backend.services.voz_service.apply_vad", return_value=dados), \
         patch("src.backend.services.voz_service.spectral_gate", return_value=dados):
        voz_service.tratar_audio("audio.wav")
        mock_write.assert_called_once()

# --- Testes para converter_webm_para_wav ---

def test_converter_webm_para_wav_erro():
    with patch("src.backend.services.voz_service.AudioSegment.from_file", side_effect=Exception("erro")):
        with pytest.raises(Exception):
            voz_service.converter_webm_para_wav("entrada.webm", "saida.wav")

# --- Testes para comparar_embeddings ---

def test_comparar_embeddings():
    emb1 = np.array([1, 0, 0])
    emb2 = np.array([1, 0, 0])
    result = voz_service.comparar_embeddings(emb1, emb2)
    assert result == 1.0

def test_comparar_embeddings_ortogonais():
    emb1 = np.array([1, 0, 0])
    emb2 = np.array([0, 1, 0])
    result = voz_service.comparar_embeddings(emb1, emb2)
    assert result == 0.0

# --- Testes para registrar_embedding_voz ---

@patch("src.backend.services.voz_service.os.path.getsize", return_value=1234)
@patch("src.backend.services.voz_service.os.path.exists", return_value=True)
@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.tratar_audio")
@patch("src.backend.services.voz_service.get_embedding")
@patch("src.backend.services.voz_service.redis_client")
@patch("src.backend.services.voz_service.os.remove")
@patch("src.backend.services.voz_service.converter_webm_para_wav")
def test_registrar_embedding_voz_sucesso(
    mock_converter, mock_remove, mock_redis, mock_get_embedding, mock_tratar, mock_copy, mock_temp,
    mock_exists, mock_getsize, mock_db, usuario, mock_upload_file
):
    temp_file = MagicMock()
    temp_file.name = "temp.webm"
    mock_temp.return_value.__enter__.return_value = temp_file
    mock_get_embedding.return_value = np.array([0.1, 0.2, 0.3])
    mock_db.query().filter_by().first.return_value = usuario

    result = voz_service.registrar_embedding_voz(1, mock_upload_file, mock_db)
    assert np.allclose(result, [0.1, 0.2, 0.3])
    mock_redis.setex.assert_called()
    mock_db.commit.assert_called_once()
    assert usuario.cadastro_completo is True
    mock_remove.assert_any_call("temp.webm")
    assert any("wav" in str(call.args[0]) for call in mock_remove.call_args_list)

@patch("src.backend.services.voz_service.os.path.getsize", return_value=1234)
@patch("src.backend.services.voz_service.os.path.exists", return_value=True)
@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.tratar_audio")
@patch("src.backend.services.voz_service.get_embedding")
@patch("src.backend.services.voz_service.redis_client")
@patch("src.backend.services.voz_service.os.remove")
@patch("src.backend.services.voz_service.converter_webm_para_wav")
def test_registrar_embedding_voz_usuario_nao_encontrado(
    mock_converter, mock_remove, mock_redis, mock_get_embedding, mock_tratar, mock_copy, mock_temp,
    mock_exists, mock_getsize, mock_db, mock_upload_file
):
    temp_file = MagicMock()
    temp_file.name = "temp.webm"
    mock_temp.return_value.__enter__.return_value = temp_file
    mock_db.query().filter_by().first.return_value = None
    mock_get_embedding.return_value = np.array([0.1, 0.2, 0.3])

    with pytest.raises(HTTPException) as exc:
        voz_service.registrar_embedding_voz(1, mock_upload_file, mock_db)
    assert exc.value.status_code == 404
    mock_remove.assert_any_call("temp.webm")
    assert any("wav" in str(call.args[0]) for call in mock_remove.call_args_list)

@patch("src.backend.services.voz_service.os.path.getsize", return_value=1234)
@patch("src.backend.services.voz_service.os.path.exists", return_value=True)
@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.tratar_audio", side_effect=ValueError("erro"))
@patch("src.backend.services.voz_service.os.remove")
@patch("src.backend.services.voz_service.converter_webm_para_wav")
def test_registrar_embedding_voz_value_error(
    mock_converter, mock_remove, mock_tratar, mock_copy, mock_temp, mock_exists, mock_getsize, mock_db, mock_upload_file
):
    temp_file = MagicMock()
    temp_file.name = "temp.webm"
    mock_temp.return_value.__enter__.return_value = temp_file

    with pytest.raises(ValueError):
        voz_service.registrar_embedding_voz(1, mock_upload_file, mock_db)
    mock_db.rollback.assert_called_once()
    mock_remove.assert_any_call("temp.webm")
    assert any("wav" in str(call.args[0]) for call in mock_remove.call_args_list)

@patch("src.backend.services.voz_service.os.path.getsize", return_value=1234)
@patch("src.backend.services.voz_service.os.path.exists", return_value=True)
@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.tratar_audio", side_effect=Exception("erro"))
@patch("src.backend.services.voz_service.os.remove")
@patch("src.backend.services.voz_service.converter_webm_para_wav")
def test_registrar_embedding_voz_erro_generico(
    mock_converter, mock_remove, mock_tratar, mock_copy, mock_temp, mock_exists, mock_getsize, mock_db, mock_upload_file
):
    temp_file = MagicMock()
    temp_file.name = "temp.webm"
    mock_temp.return_value.__enter__.return_value = temp_file

    with pytest.raises(HTTPException) as exc:
        voz_service.registrar_embedding_voz(1, mock_upload_file, mock_db)
    assert exc.value.status_code == 500
    mock_db.rollback.assert_called_once()
    mock_remove.assert_any_call("temp.webm")
    assert any("wav" in str(call.args[0]) for call in mock_remove.call_args_list)

# --- Testes para get_embedding_usuario_cache ---

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

# --- Testes para autenticar_por_voz ---

@patch("src.backend.services.voz_service.os.path.exists", return_value=True)
@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.tratar_audio")
@patch("src.backend.services.voz_service.get_embedding_usuario_cache")
@patch("src.backend.services.voz_service.get_embedding")
@patch("src.backend.services.voz_service.comparar_embeddings")
@patch("src.backend.services.voz_service.os.remove")
@patch("src.backend.services.voz_service.converter_webm_para_wav")
def test_autenticar_por_voz_sucesso(
    mock_converter, mock_remove, mock_comparar, mock_get_embedding, mock_get_cache, mock_tratar, mock_copy, mock_temp, mock_exists, mock_db, mock_upload_file
):
    temp_file = MagicMock()
    temp_file.name = "temp.webm"
    mock_temp.return_value.__enter__.return_value = temp_file
    mock_get_cache.return_value = np.array([0.1, 0.2, 0.3])
    mock_get_embedding.return_value = np.array([0.1, 0.2, 0.3])
    mock_comparar.return_value = 0.99

    result = voz_service.autenticar_por_voz(1, mock_upload_file, mock_db)
    assert result == 0.99
    mock_remove.assert_any_call("temp.webm")
    assert any("wav" in str(call.args[0]) for call in mock_remove.call_args_list)

@patch("src.backend.services.voz_service.os.path.exists", return_value=True)
@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.tratar_audio")
@patch("src.backend.services.voz_service.get_embedding_usuario_cache", return_value=None)
@patch("src.backend.services.voz_service.os.remove")
@patch("src.backend.services.voz_service.converter_webm_para_wav")
def test_autenticar_por_voz_embedding_nao_encontrado(
    mock_converter, mock_remove, mock_get_cache, mock_tratar, mock_copy, mock_temp, mock_exists, mock_db, mock_upload_file
):
    temp_file = MagicMock()
    temp_file.name = "temp.webm"
    mock_temp.return_value.__enter__.return_value = temp_file

    with pytest.raises(HTTPException) as exc:
        voz_service.autenticar_por_voz(1, mock_upload_file, mock_db)
    assert exc.value.status_code == 404
    mock_remove.assert_any_call("temp.webm")
    assert any("wav" in str(call.args[0]) for call in mock_remove.call_args_list)

@patch("src.backend.services.voz_service.os.path.exists", return_value=True)
@patch("src.backend.services.voz_service.tempfile.NamedTemporaryFile")
@patch("src.backend.services.voz_service.shutil.copyfileobj")
@patch("src.backend.services.voz_service.tratar_audio", side_effect=Exception("erro"))
@patch("src.backend.services.voz_service.os.remove")
@patch("src.backend.services.voz_service.converter_webm_para_wav")
def test_autenticar_por_voz_erro_generico(
    mock_converter, mock_remove, mock_tratar, mock_copy, mock_temp, mock_exists, mock_db, mock_upload_file
):
    temp_file = MagicMock()
    temp_file.name = "temp.webm"
    mock_temp.return_value.__enter__.return_value = temp_file

    with pytest.raises(HTTPException) as exc:
        voz_service.autenticar_por_voz(1, mock_upload_file, mock_db)
    assert exc.value.status_code == 500
    mock_remove.assert_any_call("temp.webm")
    assert any("wav" in str(call.args[0]) for call in mock_remove.call_args_list)

# --- Testes para bandpass_filter e notch_filter ---

def test_bandpass_filter_chama_butter_bandpass():
    with patch("src.backend.services.voz_service.butter_bandpass") as mock_butter:
        mock_butter.return_value = ([1,2,3], [1,2,3])
        data = np.ones(100)
        result = voz_service.bandpass_filter(data)
        assert isinstance(result, np.ndarray)

def test_notch_filter_chama_iirnotch():
    with patch("src.backend.services.voz_service.iirnotch") as mock_iirnotch:
        mock_iirnotch.return_value = ([1,2,3], [1,2,3])
        data = np.ones(100)
        result = voz_service.notch_filter(data)
        assert isinstance(result, np.ndarray)

# --- Testes para apply_vad e spectral_gate ---

def test_apply_vad_sem_voz():
    audio = np.zeros(16000)
    with patch("src.backend.services.voz_service.webrtcvad.Vad.is_speech", return_value=False):
        result = voz_service.apply_vad(audio, 16000)
        assert np.allclose(result, audio)

def test_apply_vad_com_voz():
    audio = np.ones(16000)
    with patch("src.backend.services.voz_service.webrtcvad.Vad.is_speech", return_value=True):
        result = voz_service.apply_vad(audio, 16000)
        # O resultado deve conter apenas 1s e não ser vazio
        assert np.all(result == 1)
        assert len(result) > 0
        assert len(result) <= len(audio)

def test_spectral_gate():
    audio = np.ones(16000)
    with patch("src.backend.services.voz_service.nr.reduce_noise", return_value=audio):
        result = voz_service.spectral_gate(audio, 16000)
        assert np.allclose(result, audio)