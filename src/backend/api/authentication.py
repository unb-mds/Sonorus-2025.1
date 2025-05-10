from fastapi import APIRouter, HTTPException, UploadFile, File
from src.backend.models.ecapa_model import ECAPAWrapper
import numpy as np
import soundfile as sf

auth_router = APIRouter()
ecapa_model = ECAPAWrapper()

# Simulação de um banco de dados de embeddings, substituir pelo banco real
user_embeddings = {
    "user1": np.random.rand(192),  # Substitua por embeddings reais
}

@auth_router.post("/verify-voice")
async def verify_voice(username: str, file: UploadFile = File(...)):
    if username not in user_embeddings:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Salve o áudio temporariamente
    audio_data, samplerate = sf.read(file.file)
    temp_audio_path = f"temp_{username}.wav"
    sf.write(temp_audio_path, audio_data, samplerate)

    # Verifique a biometria
    similarity_score = ecapa_model.verify_speaker(temp_audio_path, user_embeddings[username])
    if similarity_score > 0.8:  # Defina um limiar adequado
        return {"message": "Autenticação bem-sucedida", "score": similarity_score}
    else:
        raise HTTPException(status_code=401, detail="Autenticação falhou")
    
"""
para testar o endpoint:
    curl -X POST "http://127.0.0.1:8000/auth/verify-voice" \
    -H "accept: application/json" \
    -H "Content-Type: multipart/form-data" \
    -F "username=user1" \
    -F "file=@path_to_audio.wav"
"""