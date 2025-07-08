
# Documentação do Banco de Dados - Biometria de Voz  

## **Objetivo**  
Implementar a estrutura inicial do banco de dados para autenticação por voz, garantindo armazenamento seguro de dados biométricos e integração com a API.  

---

## **Estrutura do Banco**  
### Tabelas Principais:  
- **`usuarios`**: Armazena dados dos usuários (nome, email, CPF, senha hash).  
- **`perfis_voz`**: Registra modelos biométricos de voz (binário) vinculados a cada usuário.  
- **`amostras_voz`**: Armazena metadados das amostras de áudio (formato, duração, qualidade).  

### Relações:  
- `perfis_voz.usuario_id` → `usuarios.id` (1:1, com `ON DELETE CASCADE`).  
- `amostras_voz.usuario_id` → `usuarios.id` (1:N).  

---

## **Arquivos Principais**  
```plaintext
📂 database/
├── models/
│   └── models.py         # Modelos SQLAlchemy
├── scripts/
│   ├── create_tables.sql # Criação das tabelas
│   ├── sample_data.sql   # Dados de teste
│   └── backup_automatico/
│       └── backup.py     # Script de backup (Google Drive)
└── db_connection.py      # Configuração da conexão