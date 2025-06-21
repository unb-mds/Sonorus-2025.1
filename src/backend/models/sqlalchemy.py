from sqlalchemy import Column, Integer, String, Text, ARRAY, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    sobrenome = Column(String(50), nullable=False)  # <-- Adicionado
    email = Column(String(50), unique=True, nullable=False, index=True)
    senha = Column(Text, nullable=False)
    embedding = Column(ARRAY(Float), nullable=False)
    cadastro_completo = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Usuario(nome={self.nome}, sobrenome={self.sobrenome}, email={self.email})>"