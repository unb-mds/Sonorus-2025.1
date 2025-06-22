CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    sobrenome VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    embedding REAL[] NOT NULL, 
    cadastro_completo BOOLEAN DEFAULT FALSE,
    CONSTRAINT chk_embedding_not_empty CHECK (cardinality(embedding) > 0)
);