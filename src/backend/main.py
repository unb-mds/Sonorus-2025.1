from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from src.backend.database.db_connection import SessionLocal
from src.backend.api.endpoints_voz import roteador_autenticacao as wav_router
from src.backend.api.autenticacao import roteador_autenticacao as autenticacao_router
from src.backend.api.endpoints_banco import roteador_banco

app = FastAPI()

IP_DO_DROPLET = "134.199.199.123" 

origins = [
    "http://localhost:3000",
    f"http://{IP_DO_DROPLET}:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(autenticacao_router, prefix="/api")
app.include_router(wav_router, prefix="/api")
app.include_router(roteador_banco, prefix="/api")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()