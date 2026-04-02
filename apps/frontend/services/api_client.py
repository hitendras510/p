import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"


def fetch_eco_route(start: str, end: str):
    """
    Calls the backend eco-route endpoint with start/end node IDs.
    Returns the full response with eco path, shortest path, and metrics.
    """
    try:
        payload = {"start": start.strip().upper(), "end": end.strip().upper()}
        response = requests.post(
            f"{BACKEND_URL}/api/v1/eco-route",
            json=payload,
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        else:
            detail = response.json().get("detail", response.text)
            st.error(f"Backend error ({response.status_code}): {detail}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend. Make sure FastAPI is running.")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None


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
    """Quick health check against the backend health endpoint."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=3)
        return response.status_code == 200
    except Exception:
        return False
