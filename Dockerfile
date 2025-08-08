# Imagen de Python
FROM python:3.11-slim

# Establece la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copia los requisitos escritos en nuestro txt e instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el archivo .env y código fuente de la app
COPY .env .env
COPY ./app ./app

# Exponemos el puerto que usará uvicorn
EXPOSE 8000

# Comando para ejecutar la API con uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
