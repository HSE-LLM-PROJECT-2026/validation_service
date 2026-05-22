from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.config import Settings, get_settings


class GenericPayload(BaseModel):
    id: str | None = None
    name: str | None = None
    cluster_id: str | None = None
    deployment_id: str | None = None
    alias: str | None = None
    status: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def service_payload(settings: Settings) -> dict[str, Any]:
    return {
        "service": settings.service_name,
        "role": settings.service_role,
        "title": settings.service_title,
        "description": settings.service_description,
        "split_enabled": settings.service_split_enabled,
        "updated_at": now_iso(),
    }


def payload_id(payload: GenericPayload | None) -> str:
    if payload and payload.id:
        return payload.id
    if payload and payload.name:
        return payload.name
    return str(uuid4())


settings = get_settings()
app = FastAPI(title=settings.service_title, version="0.1.0")
store: dict[str, dict[str, Any]] = {}


@app.get("/livez")
async def livez() -> dict[str, Any]:
    return {"status": "ok", **service_payload(settings)}


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"status": "ok", **service_payload(settings)}


@app.get("/service-info")
async def service_info() -> dict[str, Any]:
    return {
        **service_payload(settings),
        "service_to_service_urls": settings.service_to_service_urls,
    }


def row(resource: str, item_id: str, payload: GenericPayload | None = None, **extra: Any) -> dict[str, Any]:
    data = payload.model_dump(mode="json") if payload else {}
    status_value = data.get("status") or extra.pop("status", "accepted")
    item = {
        "id": item_id,
        "resource": resource,
        "service": settings.service_name,
        "role": settings.service_role,
        "status": status_value,
        "updated_at": now_iso(),
        **extra,
    }
    for key, value in data.items():
        if key != "status" and value is not None:
            item[key] = value
    store[f"{resource}:{item_id}"] = item
    return item


def list_rows(resource: str) -> list[dict[str, Any]]:
    return [value for key, value in sorted(store.items()) if key.startswith(f"{resource}:")]


def get_row(resource: str, item_id: str) -> dict[str, Any]:
    return store.get(f"{resource}:{item_id}") or {
        "id": item_id,
        "resource": resource,
        "service": settings.service_name,
        "role": settings.service_role,
        "status": "not_found",
        "updated_at": now_iso(),
    }


@app.get("/validation/slo-configs")
async def list_slo_configs() -> Any:
    return list_rows("validation")


@app.post("/validation/slo-configs")
async def create_slo_config(payload: GenericPayload | None = None) -> Any:
    return row("validation", payload_id(payload), payload, operation="create_slo_config")


@app.get("/validation/slo-configs/{slo_config_id}")
async def get_slo_config(slo_config_id: str) -> Any:
    return get_row("validation", slo_config_id)


@app.delete("/validation/slo-configs/{slo_config_id}")
async def delete_slo_config(slo_config_id: str) -> Any:
    key = f"validation:{slo_config_id}"
    deleted = store.pop(key, None)
    if deleted:
        return deleted
    return {
        "id": slo_config_id,
        "resource": "validation",
        "service": settings.service_name,
        "role": settings.service_role,
        "status": "deleted",
        "updated_at": now_iso(),
    }


@app.get("/validation/runs")
async def list_validation_runs() -> Any:
    return list_rows("validation")


@app.post("/validation/runs")
async def create_validation_run(payload: GenericPayload | None = None) -> Any:
    return row("validation", payload_id(payload), payload, operation="create_validation_run")


@app.get("/validation/runs/{run_id}")
async def get_validation_run(run_id: str) -> Any:
    return get_row("validation", run_id)


@app.post("/validation/runs/{run_id}/cancel")
async def cancel_validation_run(run_id: str, payload: GenericPayload | None = None) -> Any:
    return row("validation", run_id, payload, operation="cancel_validation_run")


@app.get("/validation/reports/{run_id}")
async def get_validation_report(run_id: str) -> Any:
    return get_row("validation", run_id)
