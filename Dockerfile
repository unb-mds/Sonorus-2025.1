FROM python:3.10-slim as builder

# Instala as ferramentas de build necessárias
RUN apt-get update && apt-get install -y build-essential ffmpeg

WORKDIR /app

COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Estágio Final ---
FROM python:3.10-slim

# Instala ffmpeg também no estágio final
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]