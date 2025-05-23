-- Inserir usuários de teste
INSERT INTO usuarios (nome_completo, email, cpf, senha_hash) 
VALUES 
    ('João Silva', 'joao@exemplo.com', '123.456.789-09', crypt('senha123', gen_salt('bf'))),
    ('Maria Souza', 'maria@exemplo.com', '987.654.321-00', crypt('senha456', gen_salt('bf')));

-- Inserir perfis de voz
INSERT INTO perfis_voz (usuario_id, modelo_voz, hash_modelo) 
VALUES 
    (1, E'\\x0123456789ABCDEF...', sha256('modelo_joao'::bytea)),
    (2, E'\\xFEDCBA9876543210...', sha256('modelo_maria'::bytea));

-- Inserir amostras de voz
INSERT INTO amostras_voz (usuario_id, perfil_id, caminho_arquivo, duracao_seconds, formato) 
VALUES 
    (1, 1, '/amostras/joao_1.wav', 3.5, 'wav'),
    (2, 2, '/amostras/maria_1.mp3', 4.2, 'mp3');