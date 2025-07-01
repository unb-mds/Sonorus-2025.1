import os
import shutil
import tempfile
import soundfile as sf
import json
import numpy as np
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from src.backend.models.modelo_resemblyzer import ModeloResemblyzer
from src.backend.models.sqlalchemy import Usuario
from src.backend.database.redis_conex import redis_client
import librosa
import uuid
from pydub import AudioSegment
import logging
from scipy.signal import butter, lfilter, iirnotch
import webrtcvad
import noisereduce as nr

logger = logging.getLogger("voz_service")

modelo_resemblyzer = ModeloResemblyzer()

def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut=100, highcut=3800, fs=44000, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def notch_filter(data, freq=60.0, fs=44000, Q=30):

    w0 = freq / (fs / 2)

    b, a = iirnotch(w0, Q)

    y = lfilter(b, a, data)
    return y

def apply_vad(audio, sr, aggressiveness=2):
    vad = webrtcvad.Vad(aggressiveness)
    audio_pcm = (audio * 32767).astype(np.int16)
    frame_duration = 30  
    frame_length = int(sr * frame_duration / 1000)
    voiced = []
    for i in range(0, len(audio_pcm) - frame_length, frame_length):
        frame = audio_pcm[i:i+frame_length].tobytes()
        if vad.is_speech(frame, sr):
            voiced.extend(audio[i:i+frame_length])
    if len(voiced) == 0:
        return audio  
    return np.array(voiced)

def spectral_gate(audio, sr):
    noise_clip = audio[:int(sr*0.5)]
    reduced_audio = nr.reduce_noise(y=audio, sr=sr, y_noise=noise_clip, prop_decrease=0.8)
    return reduced_audio

def converter_webm_para_wav(caminho_entrada, caminho_saida, sample_rate=48000):
    try:
        audio = AudioSegment.from_file(caminho_entrada)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(sample_rate)
        audio.export(caminho_saida, format="wav", codec="pcm_s16le")
    except Exception as e:
        print(f"Erro ao converter áudio: {e}")
        raise

def get_embedding(audio_path):
    return modelo_resemblyzer.obter_embedding(audio_path)

def comparar_embeddings(embedding1, embedding2):
    return float(np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))

def tratar_audio(caminho_audio):
    dados, sr = sf.read(caminho_audio)
    duracao = len(dados) / sr
    if duracao > 30:
        raise ValueError("O áudio enviado tem mais de 30 segundos.")
    print(f"Formato recebido: shape={dados.shape}, sr={sr}")

    if len(dados.shape) > 1:
        dados = np.mean(dados, axis=1)
        print("Convertido para mono.")

    dados = bandpass_filter(dados, 100, 3800, sr)
    print("Filtro passa-banda aplicado.")

    dados = notch_filter(dados, 60.0, sr)
    print("Filtro notch 60Hz aplicado.")

    dados = apply_vad(dados, sr)
    print("VAD aplicado.")

    dados = spectral_gate(dados, sr)
    print("Spectral gating aplicado.")

    energia = np.sqrt(np.mean(dados ** 2))
    print(f"Energia RMS do áudio tratado: {energia:.6f}")
    if energia < 0.01 or duracao < 1.0:
        sf.write("debug_audio_vazio.wav", dados, sr)
        raise ValueError("O áudio tratado está vazio, muito silencioso ou muito curto. Grave novamente.")

    if dados.dtype != np.int16:
        max_abs = np.max(np.abs(dados))
        if max_abs > 1.0:
            dados = dados / max_abs  
        dados = (dados * 32767).astype(np.int16)
        print("Convertido para int16.")

    sf.write("debug_audio.wav", dados, sr, subtype='PCM_16')
    print("Áudio tratado e salvo.")

    sf.write(caminho_audio, dados, sr, subtype='PCM_16')

def registrar_embedding_voz(usuario_id: int, arquivo: UploadFile, db: Session) -> np.ndarray:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_in:
        shutil.copyfileobj(arquivo.file, temp_in)
        temp_in_path = temp_in.name

    temp_wav_path = tempfile.mktemp(suffix=".wav")
    try:
        if temp_in_path.endswith(".wav"):
            shutil.copy(temp_in_path, temp_wav_path)
        else:
            converter_webm_para_wav(temp_in_path, temp_wav_path)

        tratar_audio(temp_wav_path)
        embedding = get_embedding(temp_wav_path)

        logger.info(f"Embedding salvo para usuário {usuario_id}: {embedding[:5]}... shape={embedding.shape}")

        usuario = db.query(Usuario).filter_by(id=usuario_id).first()
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        usuario.embedding = embedding.tolist()
        usuario.cadastro_completo = True 
        db.commit()

        redis_key = f"embedding_cadastro:{usuario_id}"
        redis_client.setex(redis_key, 10800, json.dumps(embedding.tolist()))

        return embedding
    except ValueError as e:
        db.rollback()
        raise e
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar embedding: {e}")
    finally:
        if os.path.exists(temp_in_path):
            os.remove(temp_in_path)
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)

def get_embedding_usuario_cache(usuario_id: int, db: Session):
    redis_key = f"embedding_cadastro:{usuario_id}"
    embedding_cache = redis_client.get(redis_key)
    if embedding_cache:
        return np.array(json.loads(embedding_cache))

    usuario = db.query(Usuario).filter_by(id=usuario_id).first()
    if usuario and usuario.embedding:
        embedding = np.array(usuario.embedding)
        redis_client.setex(redis_key, 10800, json.dumps(embedding.tolist()))
        return embedding
    return None

def autenticar_por_voz(usuario_id: int, arquivo: UploadFile, db: Session):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_in:
        shutil.copyfileobj(arquivo.file, temp_in)
        temp_in_path = temp_in.name

    temp_wav_path = tempfile.mktemp(suffix=".wav")
    try:
        if temp_in_path.endswith(".wav"):
            shutil.copy(temp_in_path, temp_wav_path)
        else:
            converter_webm_para_wav(temp_in_path, temp_wav_path)

        tratar_audio(temp_wav_path)
        embedding_cadastro = get_embedding_usuario_cache(usuario_id, db)
        if embedding_cadastro is None:
            raise HTTPException(status_code=404, detail="Embedding do usuário não encontrado")

        embedding_tentativa = get_embedding(temp_wav_path)
        similaridade = comparar_embeddings(embedding_cadastro, embedding_tentativa)
        return similaridade
    except HTTPException:
        raise  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na autenticação por voz: {e}")
    finally:
        if os.path.exists(temp_in_path):
            os.remove(temp_in_path)
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)