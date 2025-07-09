FROM python:3.10-slim as builder

# Instala as ferramentas de build necessárias
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Estágio Final ---
FROM python:3.10-slim

WORKDIR /app

# Copia as dependências instaladas do estágio de build
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
# ADICIONE ESTA LINHA para copiar os executáveis
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia o código da aplicação
COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]