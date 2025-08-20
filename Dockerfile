# Imagem base com Python
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependência e instala
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY src/ ./src

# Define o diretório de trabalho principal
WORKDIR /app/src

# Comando para rodar a aplicação
CMD ["python", "main.py"]
