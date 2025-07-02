#!/usr/bin/env python
"""
Script para executar os testes automatizados da API do Sonorus.
Executa testes unitários para os endpoints da API usando pytest.
"""
import os
import sys
import pytest

def main():
    """Executa os testes da API."""
    print("Executando testes da API do Sonorus...")
    
    # Adiciona o diretório raiz ao PYTHONPATH para resolver importações
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
    
    # Executa os testes com pytest
    pytest.main(['-xvs', os.path.dirname(__file__)])

if __name__ == "__main__":
    main()
