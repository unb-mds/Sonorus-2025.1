# Validação do Banco de Dados

#Objetivo: garantir que os scripts de criação, migração e backup funcionam corretamente.

#Testes Realizados

- Execução do `Build.sh` para criar tabelas 
- Inserção manual de dado na tabela `usuario` 
- Backup com `pg_dump` 
- Criação de banco novo e restauração com `psql` 
- Verificação dos dados restaurados 

#Conclusão: o banco foi criado e restaurado com sucesso, sem perda de dados.


