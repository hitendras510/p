from apps.frontend.utils.formatters import (
    compute_route_summary,
    normalize_base_url,
    parse_improvement_percent,
    route_to_string,
)


def test_parse_improvement_percent():
    assert parse_improvement_percent("12.50% less pollution") == 12.5
    assert parse_improvement_percent("N/A") is None


def test_route_to_string():
    assert route_to_string(["A", "B", "F"]) == "A → B → F"


def test_compute_route_summary():
    history = [
        {"improvement": "10.00% less pollution"},
        {"improvement": "5.00% less pollution"},
        {"improvement": "N/A"},
    ]
    summary = compute_route_summary(history)
    assert summary["total_queries"] == 3
    assert summary["avg_improvement"] == 7.5


def test_normalize_base_url():
    assert normalize_base_url("http://localhost:8000/", "http://x") == "http://localhost:8000"
