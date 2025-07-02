# filepath: tests/backend/models/test_modelo_ecapa.py
import numpy as np
import pytest
from unittest.mock import patch, MagicMock

from src.backend.models.modelo_ecapa import ModeloECAPA

@patch("src.backend.models.modelo_ecapa.SpeakerRecognition")
def test_init_modelo_ecapa(mock_speaker_recognition):
    mock_instance = MagicMock()
    mock_speaker_recognition.from_hparams.return_value = mock_instance
    modelo = ModeloECAPA()
    assert modelo.modelo == mock_instance
    mock_speaker_recognition.from_hparams.assert_called_once()

@patch("src.backend.models.modelo_ecapa.read_audio")
def test_obter_embedding(mock_read_audio):
    modelo = ModeloECAPA()
    modelo.modelo = MagicMock()
    # Simula tensor de áudio
    fake_tensor = MagicMock()
    fake_tensor.unsqueeze.return_value = fake_tensor
    mock_read_audio.return_value = fake_tensor
    # Simula saída do modelo
    fake_embedding = MagicMock()
    fake_embedding.squeeze.return_value.detach.return_value.cpu.return_value.numpy.return_value = np.array([1.0, 2.0, 3.0])
    modelo.modelo.encode_batch.return_value = fake_embedding

    emb = modelo.obter_embedding("fake_path.wav")
    assert np.allclose(emb, np.array([1.0, 2.0, 3.0]))
    mock_read_audio.assert_called_once_with("fake_path.wav")
    modelo.modelo.encode_batch.assert_called_once()

@patch.object(ModeloECAPA, "obter_embedding")
def test_verificar_falante(mock_obter_embedding):
    modelo = ModeloECAPA()
    # Simula embedding de teste
    emb_teste = np.array([1.0, 0.0])
    emb_ref = np.array([0.0, 1.0])
    mock_obter_embedding.return_value = emb_teste

    score = modelo.verificar_falante("fake_path.wav", emb_ref)
    # Embeddings ortogonais: similaridade deve ser 0
    assert np.isclose(score, 0.0)
    mock_obter_embedding.assert_called_once_with("fake_path.wav")

def test_verificar_falante_mesmo_embedding():
    modelo = ModeloECAPA()
    emb = np.array([1.0, 2.0, 3.0])
    # Patch o método para retornar o mesmo embedding
    modelo.obter_embedding = lambda x: emb
    score = modelo.verificar_falante("fake_path.wav", emb)
    # Similaridade de vetores idênticos deve ser 1
    assert np.isclose(score, 1.0)