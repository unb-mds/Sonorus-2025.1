from sqlalchemy import Column, Integer, String, Text, ARRAY, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
    senha = Column(Text, nullable=False)
    embedding = Column(ARRAY(Float), nullable=False) 

    def __repr__(self):
        return f"<Usuario(nome={self.nome}, email={self.email})>"