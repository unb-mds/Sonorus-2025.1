import os
import shutil
import tempfile
import soundfile as sf
import json
import numpy as np
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from src.backend.models.modelo_ecapa import ModeloECAPA
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

modelo_ecapa = ModeloECAPA()

def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut=80, highcut=4000, fs=16000, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def notch_filter(data, freq=60.0, fs=16000, Q=30):
    """
    Aplica filtro notch para remover interferência de frequência específica (60Hz).
    
    Args:
        data: Dados de áudio
        freq: Frequência a ser removida (Hz) - padrão 60Hz (rede elétrica)
        fs: Taxa de amostragem
        Q: Fator de qualidade (maior = filtro mais estreito)
    
    Returns:
        Dados filtrados
    """
    # Calcula a frequência normalizada (0 a 1, onde 1 = Nyquist)
    w0 = freq / (fs / 2)
    
    # Cria o filtro notch IIR
    b, a = iirnotch(w0, Q)
    
    # Aplica o filtro
    filtered_data = lfilter(b, a, data)
    return filtered_data

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
    reduced_audio = nr.reduce_noise(y=audio, sr=sr, y_noise=noise_clip, prop_decrease=1.0)
    return reduced_audio

def converter_webm_para_wav(caminho_entrada, caminho_saida):
    try:
        audio = AudioSegment.from_file(caminho_entrada)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(caminho_saida, format="wav")
    except Exception as e:
        logger.error(f"Erro ao converter áudio: {e}")
        raise

def get_embedding(audio_path):
    return modelo_ecapa.obter_embedding(audio_path)

def comparar_embeddings(embedding1, embedding2):
    return float(np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))

def tratar_audio(caminho_audio):
    dados, sr = sf.read(caminho_audio)
    duracao = len(dados) / sr
    if duracao > 30:
        raise ValueError("O áudio enviado tem mais de 30 segundos.")
    logger.info(f"Formato recebido: shape={dados.shape}, sr={sr}")

    if len(dados.shape) > 1:
        dados = np.mean(dados, axis=1)
        logger.info("Convertido para mono.")

    if sr != 16000:
        logger.info(f"Convertendo taxa de amostragem de {sr} para 16000 Hz.")
        dados = librosa.resample(dados, orig_sr=sr, target_sr=16000)
        sr = 16000

    dados = bandpass_filter(dados, 80, 4000, sr)
    logger.info("Filtro passa-banda aplicado.")

    dados = notch_filter(dados, 60.0, sr)
    logger.info("Filtro notch 60Hz aplicado.")

    dados = apply_vad(dados, sr)
    logger.info("VAD aplicado.")

    dados = spectral_gate(dados, sr)
    logger.info("Spectral gating aplicado.")

    if dados.dtype != np.int16:
        if np.max(np.abs(dados)) <= 1.0:
            dados = (dados * 32767).astype(np.int16)
        else:
            dados = dados.astype(np.int16)
        logger.info("Convertido para int16.")

    sf.write(caminho_audio, dados, 16000, subtype='PCM_16')
    logger.info("Áudio tratado e salvo.")

def registrar_embedding_voz(usuario_id: int, arquivo: UploadFile, db: Session) -> np.ndarray:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_webm:
        shutil.copyfileobj(arquivo.file, temp_webm)
        temp_webm_path = temp_webm.name

    logger.info(f"Tamanho do arquivo recebido: {os.path.getsize(temp_webm_path)} bytes")
    temp_wav_path = tempfile.mktemp(suffix=".wav")
    try:
        converter_webm_para_wav(temp_webm_path, temp_wav_path)
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
        if os.path.exists(temp_webm_path):
            os.remove(temp_webm_path)
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
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_webm:
        shutil.copyfileobj(arquivo.file, temp_webm)
        temp_webm_path = temp_webm.name

    temp_wav_path = tempfile.mktemp(suffix=".wav")
    try:
        converter_webm_para_wav(temp_webm_path, temp_wav_path)
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
        if os.path.exists(temp_webm_path):
            os.remove(temp_webm_path)
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)

def remover_usuario_sem_voz(usuario_id: int, db: Session):
    """
    Remove o usuário do banco caso ocorra erro no registro de voz.
    Só remove se o cadastro não estiver completo.
    """
    usuario = db.query(Usuario).filter_by(id=usuario_id).first()
    if usuario and not usuario.cadastro_completo:
        db.delete(usuario)
        db.commit()
        logger.info(f"Usuário {usuario.email} removido por erro no registro de voz.")