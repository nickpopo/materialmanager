# Material Manager

Material Manager — это приложение на Python с графическим интерфейсом, предназначенное для управления материалами на складе. Приложение позволяет пользователям добавлять, обновлять и удалять материалы, а также просматривать отчеты о наличии материалов и экспортировать их в Excel.

## Основные функции

- Авторизация пользователей (регистрация и вход)
- Добавление, обновление и удаление материалов
- Просмотр отчета о наличии материалов
- Экспорт отчета в Excel

## Запуск
Для запуска приложения выполните:
python src/main.py

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/nickpopo/material-manager.git
   cd material-manager

2. Установите необходимые зависимости:
   pip install -r requirements.txt

3. Настройте конфигурацию базы данных в файле config.ini.

## Тестирование
Для запуска тестов используйте:
python -m unittest discover -s tests

## Структура проекта
src/ — основной код приложения:
main.py — точка входа в приложение.
gui.py — графический интерфейс пользователя.
database.py — работа с базой данных.
report.py — генерация отчетов.
tests/ — модульные тесты.
config.ini — конфигурационный файл.
requirements.txt — зависимости проекта.
README.md — документация проекта.