# Benchmark e Comparativo — Bibliotecas de Testes Unitários em Python

## Objetivo

Avaliar as três principais bibliotecas de testes unitários do ecossistema Python em uso prático: unittest, pytest e nose2. O foco está em desempenho, funcionalidades, facilidade de uso e integração com o ecossistema de desenvolvimento.

## Bibliotecas Analisadas

1. **unittest** – Biblioteca padrão do Python.
2. **pytest** – Biblioteca moderna, flexível e extensível.
3. **nose2** – Sucessora do nose, voltada à compatibilidade com unittest.

## 📊 Comparativo de Funcionalidades

| Critério                        | `unittest`| `pytest`   | `nose2`    |
|---------------------------------|-----------|------------|------------|
| **Sintaxe concisa**             | Não       | Sim        | Parcial    |
| **Fixtures poderosas**          | Limitado  | Avançado   | Sim        |
| **Parametrização**              | Limitado  | Sim        | Sim        |
| **Cobertura de código**         | Externo   | Integrável | Integrável |
| **Relatórios personalizados**   | Não       | Sim        | Parcial    |
| **Documentação**                | Boa       | Excelente  | Mediana    |
| **Manutenção ativa**            | Sim       | Sim        | Baixa      |
| **Suporte da comunidade**       | Alta      | Muito Alta | Baixa      |
| **Integração com CI/CD**        | Sim       | Excelente  | Limitada   |

## Conclusão

**Biblioteca escolhida:** pytest

### Justificativa:

- **Sintaxe simples e legível**, reduzindo esforço para escrever e manter testes.
- **Suporte avançado a fixtures e parametrização**, ideal para projetos de médio e grande porte.
- **Forte ecossistema e comunidade ativa**, o que garante longevidade e integração com DevOps.

## Referências

- [Pytest Documentation](https://docs.pytest.org/)
- [Unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Nose2 Documentation](https://nose2.readthedocs.io/)
