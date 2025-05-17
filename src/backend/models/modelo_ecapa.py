# models/ecapa_model.py

from speechbrain.pretrained import SpeakerRecognition
from speechbrain.dataio.dataio import read_audio
import torch
import numpy as np

class ModeloECAPA:
    def __init__(self):
        self.modelo = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/ecapa"
        )

    def obter_embedding(self, caminho_audio):
        # Lê o áudio e converte para tensor
        sinal = read_audio(caminho_audio)
        sinal = sinal.unsqueeze(0)  # adiciona dimensão de batch
        return self.modelo.encode_batch(sinal).squeeze().detach().cpu().numpy()

    def verificar_falante(self, caminho_audio, embedding_referencia):
        embedding_teste = self.obter_embedding(caminho_audio)
        pontuacao_similaridade = np.dot(embedding_teste, embedding_referencia) / (
            np.linalg.norm(embedding_teste) * np.linalg.norm(embedding_referencia)
        )
        return pontuacao_similaridade
