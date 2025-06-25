from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np

class ModeloResemblyzer:
    def __init__(self):
        self.encoder = VoiceEncoder()

    def obter_embedding(self, caminho_audio):
        wav = preprocess_wav(caminho_audio)
        emb = self.encoder.embed_utterance(wav)
        return emb

    def verificar_falante(self, caminho_audio, embedding_referencia):
        embedding_teste = self.obter_embedding(caminho_audio)
        # Similaridade por cosseno
        pontuacao_similaridade = np.dot(embedding_teste, embedding_referencia) / (
            np.linalg.norm(embedding_teste) * np.linalg.norm(embedding_referencia)
        )
        return pontuacao_similaridade