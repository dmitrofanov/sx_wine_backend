# Архитектура приложения SX Wine Backend

## Общая информация

**Технологический стек:**
- Django (веб-фреймворк)
- Django REST Framework (для создания REST API)
- Python 3.x

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
├── wine_api/                 # Приложение для работы с винами и связанными моделями
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
├── media/                     # Директория для медиа-файлов (изображения)
└── README.md
```

## Модели данных

### 1. Producer (Производитель)
**Поля:**
- `name` - CharField (название производителя)
- `description` - TextField (описание производителя)

**Метаданные:**
- Вербальное имя: "Производитель"
- Вербальное имя множественное: "Производители"

### 2. WineCategory (Категория вина)
**Поля:**
- `name` - CharField (название категории)

**Метаданные:**
- Вербальное имя: "Категория вина"
- Вербальное имя множественное: "Категории вин"

### 3. WineColor (Цвет вина)
**Поля:**
- `name` - CharField (название цвета, например: красное, белое, розовое)

**Метаданные:**
- Вербальное имя: "Цвет вина"
- Вербальное имя множественное: "Цвета вин"

### 4. WineSugar (Содержание сахара в вине)
**Поля:**
- `name` - CharField (название, например: сухое, полусухое, сладкое)

**Метаданные:**
- Вербальное имя: "Содержание сахара"
- Вербальное имя множественное: "Содержание сахара"

### 5. Country (Страна)
**Поля:**
- `name` - CharField (название страны)

**Метаданные:**
- Вербальное имя: "Страна"
- Вербальное имя множественное: "Страны"

### 6. Region (Регион)
**Поля:**
- `name` - CharField (название региона)

**Метаданные:**
- Вербальное имя: "Регион"
- Вербальное имя множественное: "Регионы"

### 7. Wine (Вино)
**Поля:**
- `name` - CharField (название вина)
- `image` - ImageField (изображение вина)
- `saved` - BooleanField (флаг сохранения/избранного)
- `category` - ForeignKey к WineCategory (категория вина)
- `sugar` - ForeignKey к WineSugar (содержание сахара)
- `country` - ForeignKey к Country (страна происхождения)
- `region` - ForeignKey к Region (регион происхождения)
- `volume` - FloatField (объем бутылки в литрах)
- `producer` - ForeignKey к Producer (производитель)
- `price` - IntegerField (цена)
- `aging` - IntegerField (выдержка в годах)
- `description` - TextField (описание вина)

**Метаданные:**
- Вербальное имя: "Вино"
- Вербальное имя множественное: "Вина"

**Связи:**
- Многие-ко-многим с Event через поле `wine_list`

### 8. City (Город)
**Поля:**
- `name` - CharField (название города)

**Метаданные:**
- Вербальное имя: "Город"
- Вербальное имя множественное: "Города"

### 9. Event (Событие)
**Поля:**
- `name` - CharField (название события)
- `date` - DateField (дата события)
- `city` - ForeignKey к City (город проведения)
- `place` - CharField (место проведения)
- `address` - CharField (адрес)
- `price` - IntegerField (цена билета)
- `available` - IntegerField (количество доступных билетов)
- `producer` - ForeignKey к Producer (производитель, связанный с событием)
- `image` - ImageField (изображение события)
- `wine_list` - ManyToManyField к Wine (список вин, представленных на событии)

**Метаданные:**
- Вербальное имя: "Событие"
- Вербальное имя множественное: "События"

## Диаграмма связей моделей

```
Producer
  ├── Wine (producer)
  └── Event (producer)

WineCategory
  └── Wine (category)

WineSugar
  └── Wine (sugar)

Country
  └── Wine (country)

Region
  └── Wine (region)

City
  └── Event (city)

Wine
  ├── Producer (producer)
  ├── WineCategory (category)
  ├── WineSugar (sugar)
  ├── Country (country)
  ├── Region (region)
  └── Event (wine_list, ManyToMany)

Event
  ├── City (city)
  ├── Producer (producer)
  └── Wine (wine_list, ManyToMany)
```

## REST API Endpoints

**Важно:** API предоставляет только GET endpoints для чтения данных. Все модификации данных (создание, обновление, удаление) осуществляются через админ-панель Django.

### Producer (Производители)
- `GET /api/producers/` - список всех производителей (возвращает все записи)
- `GET /api/producers/{id}/` - детали конкретного производителя

### WineCategory (Категории вин)
- `GET /api/categories/` - список всех категорий (возвращает все записи)
- `GET /api/categories/{id}/` - детали конкретной категории

### WineColor (Цвета вин)
- `GET /api/colors/` - список всех цветов (возвращает все записи)
- `GET /api/colors/{id}/` - детали конкретного цвета

### WineSugar (Содержание сахара)
- `GET /api/sugars/` - список всех типов сахара (возвращает все записи)
- `GET /api/sugars/{id}/` - детали конкретного типа

### Country (Страны)
- `GET /api/countries/` - список всех стран (возвращает все записи)
- `GET /api/countries/{id}/` - детали конкретной страны

### Region (Регионы)
- `GET /api/regions/` - список всех регионов (возвращает все записи)
- `GET /api/regions/{id}/` - детали конкретного региона

### Wine (Вино)
- `GET /api/wines/` - список всех вин (возвращает все записи, с фильтрацией)
- `GET /api/wines/{id}/` - детали конкретного вина

**Параметры фильтрации для Wine:**
- `GET /api/wines/?saved=true` - фильтрация по сохраненным винам
- `GET /api/wines/?category={id}` - фильтрация по категории
- `GET /api/wines/?producer={id}` - фильтрация по производителю
- `GET /api/wines/?country={id}` - фильтрация по стране
- `GET /api/wines/?region={id}` - фильтрация по региону
- `GET /api/wines/?price_min={value}&price_max={value}` - фильтрация по цене

### City (Города)
- `GET /api/cities/` - список всех городов (возвращает все записи)
- `GET /api/cities/{id}/` - детали конкретного города

### Event (События)
- `GET /api/events/` - список всех событий (возвращает все записи, с фильтрацией)
- `GET /api/events/{id}/` - детали конкретного события

**Параметры фильтрации для Event:**
- `GET /api/events/?city={id}` - фильтрация по городу
- `GET /api/events/?producer={id}` - фильтрация по производителю
- `GET /api/events/?date_from={date}&date_to={date}` - фильтрация по дате
- `GET /api/events/?available=true` - только события с доступными билетами

## Сериализаторы (Serializers)

Для каждой модели будет создан соответствующий сериализатор:
- `ProducerSerializer` - для Producer
- `WineCategorySerializer` - для WineCategory
- `WineColorSerializer` - для WineColor
- `WineSugarSerializer` - для WineSugar
- `CountrySerializer` - для Country
- `RegionSerializer` - для Region
- `WineSerializer` - для Wine (с вложенными объектами для связанных моделей)
- `CitySerializer` - для City
- `EventSerializer` - для Event (с вложенными объектами для связанных моделей)

## Представления (Views)

Использование ReadOnlyViewSet из Django REST Framework (только чтение данных):
- `ProducerViewSet` - для Producer (ReadOnlyViewSet)
- `WineCategoryViewSet` - для WineCategory (ReadOnlyViewSet)
- `WineColorViewSet` - для WineColor (ReadOnlyViewSet)
- `WineSugarViewSet` - для WineSugar (ReadOnlyViewSet)
- `CountryViewSet` - для Country (ReadOnlyViewSet)
- `RegionViewSet` - для Region (ReadOnlyViewSet)
- `WineViewSet` - для Wine (ReadOnlyViewSet с фильтрацией)
- `CityViewSet` - для City (ReadOnlyViewSet)
- `EventViewSet` - для Event (ReadOnlyViewSet с фильтрацией)

## Фильтрация и поиск

### Wine
- Фильтрация по: category, sugar, country, region, producer, price (диапазон), saved
- Поиск по: name, description
- **Важно:** Все данные возвращаются без пагинации

### Event
- Фильтрация по: city, producer, date (диапазон), available
- Поиск по: name, place, address
- **Важно:** Все данные возвращаются без пагинации

## Настройки медиа-файлов

- `MEDIA_ROOT` - директория для хранения загруженных изображений
- `MEDIA_URL` - URL для доступа к медиа-файлам
- Поддержка загрузки изображений для моделей Wine и Event

## Админ-панель Django

**Важно:** Админ-панель является единственным способом модификации данных (создание, обновление, удаление записей).

Все модели будут зарегистрированы в админ-панели для управления данными:
- Producer
- WineCategory
- WineColor
- WineSugar
- Country
- Region
- Wine
- City
- Event

Админ-панель доступна по адресу: `/admin/`

## Безопасность

- CORS настройки для работы с фронтендом (django-cors-headers)
- Разрешения доступа (Permissions) - только чтение для API endpoints
- Валидация данных через сериализаторы
- Защита секретных данных через переменные окружения

## База данных

- **PostgreSQL** - основная база данных
- База данных запускается в Docker контейнере через docker-compose
- Настройки подключения к БД через переменные окружения

## Docker и Docker Compose

### Структура Docker

**Dockerfile:**
- Базовый образ: Python 3.x
- Установка зависимостей из requirements.txt
- Копирование проекта
- Настройка рабочей директории
- Запуск Django приложения

**docker-compose.yml:**
- Сервис `db` - PostgreSQL контейнер
- Сервис `web` - Django приложение
- Настройка volumes для:
  - Медиа-файлов (изображения)
  - Постоянного хранения данных БД
- Настройка сетей для связи между контейнерами
- Переменные окружения для конфигурации

**Переменные окружения (.env):**
- `POSTGRES_DB` - название базы данных
- `POSTGRES_USER` - пользователь PostgreSQL
- `POSTGRES_PASSWORD` - пароль PostgreSQL
- `DATABASE_HOST` - хост базы данных (db)
- `DATABASE_PORT` - порт базы данных (5432)
- `SECRET_KEY` - секретный ключ Django
- `DEBUG` - режим отладки
- `ALLOWED_HOSTS` - разрешенные хосты

### Команды для работы с Docker

- `docker-compose up` - запуск всех сервисов
- `docker-compose up -d` - запуск в фоновом режиме
- `docker-compose down` - остановка всех сервисов
- `docker-compose exec web python manage.py migrate` - выполнение миграций
- `docker-compose exec web python manage.py createsuperuser` - создание суперпользователя
- `docker-compose exec web python manage.py collectstatic` - сбор статических файлов

## Дополнительные возможности (для будущей реализации)

- Аутентификация и авторизация пользователей
- Избранные вина для пользователей
- Рейтинги и отзывы на вина
- История покупок
- Уведомления о событиях

