from speechbrain.inference.speaker import SpeakerRecognition
from speechbrain.dataio.dataio import read_audio

model = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

def get_embedding(audio_path):
    waveform = read_audio(audio_path)
    embedding = model.encode_batch(waveform).squeeze().detach().cpu().numpy()
    return embedding

embedding = get_embedding("../../../lemes.wav")
print("Embedding extraído:")
print(embedding)
