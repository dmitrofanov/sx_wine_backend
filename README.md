# SX Wine Backend

REST API backend для приложения SX Wine на Django и Django REST Framework.

## Технологический стек

- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL 15
- Docker & Docker Compose

## Структура проекта

```
sx_wine_backend/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .dockerignore
├── sx_wine_backend/          # Главный проект Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── wine_api/                 # Приложение для работы с винами
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
└── media/                     # Директория для медиа-файлов
```

## Быстрый старт

### 1. Клонирование и настройка

```bash
# Скопируйте .env.example в .env
cp .env.example .env

# Отредактируйте .env файл при необходимости
```

### 2. Запуск с Docker Compose

```bash
# Запуск всех сервисов
docker-compose up -d

# Выполнение миграций
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser
```

### 3. Доступ к приложению

- API: http://localhost:8000/api/
- Админ-панель: http://localhost:8000/admin/

## API Endpoints

### Wine (Вино)
- `GET /api/wines/` - список всех вин
- `GET /api/wines/{id}/` - детали конкретного вина

### Event (События)
- `GET /api/events/` - список всех событий
- `GET /api/events/{id}/` - детали конкретного события

**Важно:** API предоставляет только GET endpoints для чтения данных. Все модификации данных осуществляются через админ-панель Django.

## Модели данных

1. **Producer** - Производитель
2. **WineCategory** - Категория вина
3. **WineColor** - Цвет вина
4. **WineSugar** - Содержание сахара
5. **Country** - Страна
6. **Region** - Регион
7. **Wine** - Вино
8. **City** - Город
9. **Event** - Событие

## Команды Docker

```bash
# Запуск в фоновом режиме
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Просмотр логов
docker-compose logs -f

# Выполнение миграций
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Сбор статических файлов
docker-compose exec web python manage.py collectstatic --noinput

# Доступ к shell Django
docker-compose exec web python manage.py shell
```

## Разработка

Для локальной разработки без Docker:

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt

# Настройка базы данных (требуется запущенный PostgreSQL)
# Обновите настройки в .env файле

# Выполнение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера разработки
python manage.py runserver
```

## Лицензия

Проект создан для SX Wine.

