from __future__ import annotations

import os
from typing import Any

import requests

from apps.frontend.utils.formatters import normalize_base_url

DEFAULT_BASE_URL = os.getenv("ECONAV_API_URL", "http://localhost:8000")


def fetch_eco_route(start: str, end: str, base_url: str | None = None) -> dict[str, Any]:
    url = normalize_base_url(base_url, DEFAULT_BASE_URL)
    payload = {"start": start.strip().upper(), "end": end.strip().upper()}
    response = requests.post(f"{url}/api/v1/eco-route", json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_health(base_url: str | None = None) -> dict[str, Any]:
    url = normalize_base_url(base_url, DEFAULT_BASE_URL)
    response = requests.get(f"{url}/health", timeout=5)
    response.raise_for_status()
    return response.json()
