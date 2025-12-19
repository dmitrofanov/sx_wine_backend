FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements.txt и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание директории для медиа-файлов
RUN mkdir -p /app/media

# Команда по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

