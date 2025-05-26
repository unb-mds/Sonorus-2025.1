-- Criação da tabela 'usuarios' (removido CPF, adicionado coluna de embedding)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    embedding REAL[] NOT NULL,                        -- vetor de embedding
    data_cadastro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    ultimo_login TIMESTAMP WITH TIME ZONE
);

-- *Removida* a tabela 'perfis_voz' conforme indicado.

-- Criação da tabela 'amostras_voz' (removida a coluna perfil_id e sua FK)
CREATE TABLE amostras_voz (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    caminho_arquivo VARCHAR(255),
    duracao_seconds DECIMAL(5,2),
    formato VARCHAR(10),
    data_captura TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    qualidade_amostra DECIMAL(3,1)
);

-- Índices para otimização
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_amostras_voz_usuario ON amostras_voz(usuario_id);
