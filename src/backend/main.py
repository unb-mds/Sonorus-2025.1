from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.backend.database.db_connection import SessionLocal
from src.backend.api.endpoints_voz import roteador_autenticacao as wav_router
from src.backend.api.autenticacao import roteador_autenticacao as autenticacao_router
from src.backend.api.endpoints_banco import roteador_banco

app = FastAPI()

app.include_router(autenticacao_router)

app.include_router(wav_router)

app.include_router(roteador_banco)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()