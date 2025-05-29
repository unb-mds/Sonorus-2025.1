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

modelo_ecapa = ModeloECAPA()

def get_embedding(audio_path):
    """
    Extrai o embedding do áudio usando o modelo ECAPA.
    """
    return modelo_ecapa.obter_embedding(audio_path)

def comparar_embeddings(embedding1, embedding2):
    """
    Calcula a similaridade cosseno entre dois embeddings.
    """
    return float(np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))

def validar_e_normalizar_audio(caminho_audio):
    dados, sr = sf.read(caminho_audio)
    print(f"Formato recebido: shape={dados.shape}, sr={sr}")

    if len(dados.shape) > 1:
        dados = np.mean(dados, axis=1)
        print("Convertido para mono.")

    if sr != 16000:
        raise ValueError("O áudio deve ter taxa de amostragem de 16kHz.")

    if dados.dtype != np.int16:
        if np.max(np.abs(dados)) <= 1.0:
            dados = (dados * 32767).astype(np.int16)
        else:
            dados = dados.astype(np.int16)
        print("Convertido para int16.")

    sf.write(caminho_audio, dados, 16000, subtype='PCM_16')
    print("Áudio normalizado e salvo.")

def registrar_embedding_voz(usuario_id: int, arquivo: UploadFile, db: Session):
    """
    Atualiza o embedding do usuário na tabela usuario.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        shutil.copyfileobj(arquivo.file, temp_audio)
        temp_audio_path = temp_audio.name

    try:
        validar_e_normalizar_audio(temp_audio_path)
        embedding = get_embedding(temp_audio_path)

        redis_key = f"embedding_cadastro:{usuario_id}"
        redis_client.setex(redis_key, 10800, json.dumps(embedding.tolist()))

        usuario = db.query(Usuario).filter_by(id=usuario_id).first()
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        usuario.embedding = embedding.tolist()
        db.commit()
        return embedding
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar embedding: {e}")
    finally:
        os.remove(temp_audio_path)

def get_embedding_usuario_cache(usuario_id: int, db: Session):
    """
    Busca o embedding do usuário no Redis ou banco de dados.
    """
    redis_key = f"embedding_cadastro:{usuario_id}"
    embedding_cache = redis_client.get(redis_key)
    if embedding_cache:
        return np.array(json.loads(embedding_cache))

    amostra = db.query(AmostraVoz).filter_by(usuario_id=usuario_id).order_by(AmostraVoz.id.desc()).first()
    if amostra:
        embedding = np.array(amostra.embedding)
        redis_client.setex(redis_key, 10800, json.dumps(embedding.tolist()))
        return embedding
    return None

def autenticar_por_voz(usuario_id: int, arquivo: UploadFile, db: Session):
    """
    Autentica o usuário comparando o embedding do áudio enviado com o embedding cadastrado.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        shutil.copyfileobj(arquivo.file, temp_audio)
        temp_audio_path = temp_audio.name

    try:
        validar_e_normalizar_audio(temp_audio_path)
        embedding_cadastro = get_embedding_usuario_cache(usuario_id, db)
        if embedding_cadastro is None:
            raise HTTPException(status_code=404, detail="Embedding do usuário não encontrado")

        embedding_tentativa = get_embedding(temp_audio_path)
        similaridade = comparar_embeddings(embedding_cadastro, embedding_tentativa)
        return similaridade
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na autenticação por voz: {e}")
    finally:
        os.remove(temp_audio_path)