# Лабораторная работа №3: Сервис для прослушивания музыки

# Описание проекта
Реализация музыкального стримингового сервиса с использованием:
- **FastAPI** - веб-фреймворк
- **SQLModel** - ORM для работы с БД
- **PostgreSQL** - СУБД
- **Python 3.8+**

# Требования
- Python 3.8 или выше
- PostgreSQL 15+
- pip (менеджер пакетов Python)

# Установка и настройка

# 1. Клонирование репозитория
git clone https://github.com/your-username/music-service-lab3.git
cd music-service-lab3

# 2. Установка зависимостей
pip install -r requirements.txt

# 3. Настройка базы данных PostgreSQL
Установите PostgreSQL

Создайте базу данных:

CREATE DATABASE music_service;
Создайте файл .env в корне проекта:

# .env
DATABASE_URL=postgresql://postgres:ваш_пароль@localhost:5432/music_service

# 4. Инициализация базы данных
python init_db.py

# 5. Запуск приложения
python main.py

# После запуска сервера откройте в браузере:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc