# src/backend/database/db_connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://biometria_user:senha_segura@localhost:5432/biometria_vocal"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # Mantido para compatibilidade com os modelos