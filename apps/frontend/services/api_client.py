<<<<<<< HEAD
import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8001"


def fetch_eco_routes(routes: list):
    """
    Sends a list of candidate routes to the backend for AI scoring.
    Returns the best route and all scored routes.
    """
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/eco-route",
            json={"routes": routes},
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Backend returned status {response.status_code}")
            return {"best_route": None, "all_routes": routes}
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend. Make sure FastAPI is running on port 8001.")
        return {"best_route": None, "all_routes": routes}
    except Exception as e:
        st.error(f"Error: {e}")
        return {"best_route": None, "all_routes": routes}


def trigger_training():
    """Triggers the model training via the backend endpoint."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/train/trigger",
            timeout=120,
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"Server returned {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "message": "Cannot connect to backend. Is FastAPI running?"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def check_backend_health():
    """Quick health check against the backend root endpoint."""
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=3)
        return response.status_code == 200
    except Exception:
        return False
=======
from __future__ import annotations

import os
from typing import Any

import requests

DEFAULT_BASE_URL = os.getenv("ECONAV_API_URL", "http://localhost:8000")


def fetch_eco_route(start: str, end: str, base_url: str | None = None) -> dict[str, Any]:
    url = (base_url or DEFAULT_BASE_URL).rstrip("/")
    payload = {"start": start.strip().upper(), "end": end.strip().upper()}
    response = requests.post(f"{url}/api/v1/eco-route", json=payload, timeout=10)
    response.raise_for_status()
    return response.json()
>>>>>>> 8c3d578ab632eedee7d285f7a1cce0c2f1edc61d
