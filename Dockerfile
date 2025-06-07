# backend/Dockerfile
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Archivos estáticos
RUN python manage.py collectstatic --noinput


EXPOSE 8000

# Usa Gunicorn para producción

CMD ["sh", "-c", "python manage.py migrate && python manage.py shell < create_superuser.py && python manage.py runserver 0.0.0.0:8000"]
