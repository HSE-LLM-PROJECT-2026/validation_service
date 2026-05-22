# Validation Service

## Описание

Сервис SLO-конфигов и запусков валидации перед переводом deployment в рабочее состояние.

## Основные возможности

- CRUD SLO-конфигов
- запуск и отмена validation run
- выдача отчета по run

## Структура проекта

- `app/` - код сервиса (FastAPI, config, domain handlers)
- `deploy/` - служебные файлы для роли сервиса в деплое
- `pyproject.toml` - зависимости и метаданные проекта
- `Dockerfile` - сборка контейнера
- `.env.example` - пример переменных окружения

## Быстрый старт (локально)

1. Установить зависимости:
   `uv sync --frozen --extra dev`
2. Запустить сервис:
   `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. Проверить health:
   `curl http://127.0.0.1:8000/health`

## Переменные окружения

- `SERVICE_ROLE` - роль сервиса в control plane
- `SERVICE_NAME` - техническое имя сервиса
- `POSTGRES_DSN` - строка подключения к PostgreSQL
- `PROMETHEUS_BASE_URL` - адрес Prometheus
- `SERVICE_TO_SERVICE_URLS_JSON` - карта внутренних URL сервисов

## Docker

- Сборка: `docker build -t validation_service:local .`
- Запуск: `docker run --rm -p 8000:8000 --env-file .env validation_service:local`

## Деплой

Файлы для деплоя лежат в `deploy/`.

## Основные API ручки

- `GET /validation/slo-configs`
- `POST /validation/slo-configs`
- `GET /validation/runs`
- `POST /validation/runs`
- `POST /validation/runs/{run_id}/cancel`
- `GET /validation/reports/{run_id}`
