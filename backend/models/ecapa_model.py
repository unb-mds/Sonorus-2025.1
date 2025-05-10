# models/ecapa_model.py
# deploy do modelo ECAPA-TDNN do SpeechBrain e gera embeddings de voz

from speechbrain.pretrained import SpeakerRecognition
import numpy as np

class ECAPAWrapper:
    def __init__(self):
        self.model = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/ecapa"
        )

    def get_embedding(self, audio_path):
        return self.model.encode_batch(audio_path).squeeze().detach().cpu().numpy()

    def verify_speaker(self, audio_path, reference_embedding):
        test_embedding = self.get_embedding(audio_path)
        similarity_score = np.dot(test_embedding, reference_embedding) / (
            np.linalg.norm(test_embedding) * np.linalg.norm(reference_embedding)
        )
        return similarity_score