from __future__ import annotations


def parse_improvement_percent(improvement: str) -> float | None:
    if not improvement or improvement == "N/A":
        return None
    token = improvement.split("%", maxsplit=1)[0].strip()
    try:
        return float(token)
    except ValueError:
        return None


def route_to_string(path: list[str]) -> str:
    return " → ".join(path)


def compute_route_summary(history: list[dict]) -> dict[str, float | int]:
    if not history:
        return {"total_queries": 0, "avg_improvement": 0.0}

    parsed = [
        parse_improvement_percent(item.get("improvement", "N/A"))
        for item in history
        if parse_improvement_percent(item.get("improvement", "N/A")) is not None
    ]

    avg = round(sum(parsed) / len(parsed), 2) if parsed else 0.0
    return {"total_queries": len(history), "avg_improvement": avg}


def normalize_base_url(base_url: str, fallback: str) -> str:
    return (base_url or fallback).strip().rstrip("/")
