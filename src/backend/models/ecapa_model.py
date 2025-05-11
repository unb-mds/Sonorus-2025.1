# models/ecapa_model.py

from speechbrain.pretrained import SpeakerRecognition
from speechbrain.dataio.dataio import read_audio
import torch
import numpy as np

class ECAPAWrapper:
    def __init__(self):
        self.model = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/ecapa"
        )

    def get_embedding(self, audio_path):
        # Lê o áudio e converte para tensor
        signal = read_audio(audio_path)
        signal = signal.unsqueeze(0)  # adiciona dimensão de batch
        return self.model.encode_batch(signal).squeeze().detach().cpu().numpy()

    def verify_speaker(self, audio_path, reference_embedding):
        test_embedding = self.get_embedding(audio_path)
        similarity_score = np.dot(test_embedding, reference_embedding) / (
            np.linalg.norm(test_embedding) * np.linalg.norm(reference_embedding)
        )
        return similarity_score
