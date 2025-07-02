# Testes Automatizados da API Sonorus

Este diretório contém os testes automatizados para os endpoints da API do Sonorus, garantindo que a camada de API esteja funcionando corretamente independentemente da lógica interna dos serviços.

## Estrutura dos Testes

- `conftest.py`: Configuração do ambiente de testes, incluindo fixtures para o cliente de teste e mocks do banco de dados.
- `test_autenticacao.py`: Testes para os endpoints de autenticação (registro, login, verificação de email).
- `test_endpoints_voz.py`: Testes para os endpoints de biometria de voz (registro e autenticação por voz).
- `test_endpoints_banco.py`: Testes para os endpoints de conexão com o banco de dados.
- `run_tests.py`: Script para executar todos os testes.

## Como Executar os Testes

### Pré-requisitos

- Python 3.8 ou superior
- Dependências do projeto instaladas (`pip install -r requirements.txt`)
- Dependências adicionais para testes: `pytest`, `pytest-cov`

### Instalação das Dependências de Teste

```bash
pip install pytest pytest-cov
```

### Executando os Testes

Para executar todos os testes:

```bash
python src/backend/tests/run_tests.py
```

Ou usando pytest diretamente:

```bash
pytest src/backend/tests -v
```

Para executar um arquivo de teste específico:

```bash
pytest src/backend/tests/test_autenticacao.py -v
```

Para gerar um relatório de cobertura:

```bash
pytest src/backend/tests --cov=src/backend/api
```

## Abordagem de Testes

### Mocking

Os testes utilizam o módulo `unittest.mock` para isolar a camada de API dos serviços subjacentes. Isso permite testar os endpoints independentemente da lógica de negócios e do banco de dados.

### Cenários Testados

- **Cenários de Sucesso**: Verificam se os endpoints retornam os códigos de status e respostas esperados quando tudo funciona corretamente.
- **Cenários de Erro**: Verificam se os endpoints lidam adequadamente com entradas inválidas, erros de autenticação e outros problemas.

### Banco de Dados

Os testes utilizam um banco de dados SQLite em memória para simular o PostgreSQL, garantindo que os testes sejam rápidos e não dependam de um banco de dados externo.

## Manutenção dos Testes

Ao modificar os endpoints da API, certifique-se de atualizar os testes correspondentes para garantir que a cobertura de testes permaneça adequada.

## Integração Contínua

Estes testes podem ser executados como parte de um pipeline de CI/CD para garantir que as alterações na API não quebrem a funcionalidade existente.
