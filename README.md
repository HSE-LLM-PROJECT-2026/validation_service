# Validation Service

## Описание

FastAPI-сервис для проверки моделей перед переводом deployment в рабочее состояние. Сервис хранит SLO-конфиги и запускает validation runs для конкретных развертываний.

## Основные возможности

- каталог SLO-конфигов
- создание validation run
- получение отчета по проверке
- отмена validation run
- служебные health/livez/service-info ручки

## Основные API-ручки

- `/validation/slo-configs`
- `/validation/runs`
- `/validation/runs/{run_id}`
- `/validation/runs/{run_id}/cancel`

## Структура проекта

- `app/` — код FastAPI-сервиса
- `app/main.py` — HTTP API и базовая service runtime логика
- `app/config.py` — настройки сервиса через переменные окружения
- `deploy/` — файлы для раскатки сервиса
- `Dockerfile` — сборка контейнера
- `pyproject.toml`, `uv.lock` — зависимости Python
- `.env.example` — пример конфигурации

## Быстрый старт локально

1. Установить зависимости:
   ```bash
   uv sync --frozen
   ```

2. Запустить сервис:
   ```bash
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Проверить, что сервис живой:
   ```bash
   curl http://localhost:8000/health
   ```

## Переменные окружения

- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` — подключение к PostgreSQL
- `K8S_NAMESPACE` — namespace платформы в Kubernetes
- `SECURITY_AUDIT_BASE_URL` — адрес security/audit service
- `SECURITY_AUDIT_SERVICE_TOKEN` — service-to-service токен
- `STATUS_PROMETHEUS_BASE_URL` — адрес Prometheus для сервисов, которым нужны метрики
- `IMAGE_REPOSITORY`, `IMAGE_TAG`, `RELEASE_NAME`, `KUBECONFIG_PATH` — параметры deploy-скриптов

Полный пример лежит в `.env.example`.

## Docker

```bash
docker build -t awesomecosmonaut/validation_service:latest .
docker run --env-file .env -p 8000:8000 awesomecosmonaut/validation_service:latest
```

## Деплой

Файлы для раскатки лежат в `deploy/`.

```bash
cd deploy
./deploy-from-scratch.sh
```

Если нужно пересобрать образ и полностью переустановить сервис:

```bash
cd deploy
./rebuild-delete-deploy.sh
```

## Автор

Igor Malysh
