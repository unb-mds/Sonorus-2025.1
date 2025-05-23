-- Criação da tabela 'usuarios'
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    cpf VARCHAR(14) UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    data_cadastro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    ultimo_login TIMESTAMP WITH TIME ZONE
);

-- Criação da tabela 'perfis_voz'
CREATE TABLE perfis_voz (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
    modelo_voz BYTEA NOT NULL,
    hash_modelo VARCHAR(64),
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ultima_atualizacao TIMESTAMP WITH TIME ZONE,
    quantidade_amostras INTEGER DEFAULT 1
);

-- Criação da tabela 'amostras_voz'
CREATE TABLE amostras_voz (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    perfil_id INTEGER REFERENCES perfis_voz(id) ON DELETE CASCADE,
    caminho_arquivo VARCHAR(255),
    duracao_seconds DECIMAL(5,2),
    formato VARCHAR(10),
    data_captura TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    qualidade_amostra DECIMAL(3,1)
);

-- Índices para otimização
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_amostras_voz_usuario ON amostras_voz(usuario_id);