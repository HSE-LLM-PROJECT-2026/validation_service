# Validation Service

## Описание

Этот репозиторий содержит сервис проверки модели перед переводом deployment в рабочее состояние. Сервис хранит SLO-конфиги, запускает validation runs и возвращает verdict для deployment service.

## Основные возможности
- каталог SLO-конфигов
- создание validation run для deployment
- получение отчета по проверке
- отмена validation run
- сбор метрик из Prometheus
- служебные health/livez/service-info ручки

## Структура проекта

- `app/` — основной код приложения
  - `main.py` — FastAPI-приложение и HTTP-ручки
  - `config.py` — настройки сервиса

- `deploy/` — файлы и переменные для развертывания
- `.env.example` — пример переменных окружения
- `Dockerfile` — сборка Docker-образа
- `pyproject.toml` — зависимости и настройки Python-проекта
- `requirements.txt` — список зависимостей для совместимого запуска без uv

## Быстрый старт локально

1. Установите зависимости:
   ```bash
   uv sync
   ```

2. Создайте `.env` на основе `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Запустите сервис:
   ```bash
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

Если `uv` не используется, можно запустить через обычный virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Переменные окружения
- `DATABASE_URL`
- `PROMETHEUS_URL`
- `DEPLOYMENT_SERVICE_URL`
- `SECURITY_SERVICE_URL`
- `SERVICE_TOKEN`
- `LOG_LEVEL`

Пример `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/llm_platform
SERVICE_TOKEN=change-me
LOG_LEVEL=INFO
```

## Основные API-ручки

| Метод | Ручка | Назначение |
|--------|-------|------------|
| `GET` | `/health` | Проверяет доступность validation service. |
| `GET` | `/livez` | Liveness probe контейнера. |
| `GET` | `/service-info` | Возвращает служебную информацию о сервисе валидации. |
| `GET` | `/validation/slo-configs` | Возвращает доступные SLO-конфиги для формы деплоя и проверки модели. |
| `POST` | `/validation/slo-configs` | Создает SLO-конфиг с порогами TTFT, TPS, TPOT, error rate и очереди. |
| `GET` | `/validation/slo-configs/{slo_config_id}` | Возвращает конкретный SLO-конфиг по идентификатору. |
| `DELETE` | `/validation/slo-configs/{slo_config_id}` | Отключает или удаляет SLO-конфиг, если он больше не нужен. |
| `GET` | `/validation/runs` | Возвращает историю запусков валидации. |
| `POST` | `/validation/runs` | Создает validation run для конкретного deployment после поднятия модели. |
| `GET` | `/validation/runs/{run_id}` | Возвращает статус validation run: pending, running, passed, failed или cancelled. |
| `POST` | `/validation/runs/{run_id}/cancel` | Отменяет активную проверку модели. |
| `GET` | `/validation/reports/{run_id}` | Возвращает отчет по метрикам и итоговый verdict проверки. |

## Сборка и запуск в Docker

```bash
docker build -t hse-llm-project-2026/validation_service:local .
docker run --env-file .env -p 8000:8000 hse-llm-project-2026/validation_service:local
```

## Деплой в Kubernetes

Файлы развертывания лежат в папке `deploy/`. Для сервисов, которые уже подключены к стенду, используются Helm values и deploy-скрипты из соответствующего репозитория или общего инфраструктурного пайплайна.

## Метрики и документация

- Swagger UI: `/docs`
- OpenAPI: `/openapi.json`
- Health check: `/health`
- Liveness check: `/livez`

## Автор

Igor Malysh
