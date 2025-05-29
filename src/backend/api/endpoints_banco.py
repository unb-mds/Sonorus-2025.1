from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.backend.database.db_connection import get_db

roteador_banco = APIRouter()

@roteador_banco.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    return {"status": "Conectado ao PostgreSQL!"}