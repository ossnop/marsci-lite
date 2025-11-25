# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_analyze_success():
    payload = {"kpi":"CTR", "values":[0.01,0.012,0.011,0.013,0.012]}
    r = client.post("/analyze", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert j["kpi"] == "CTR"
    assert j["benchmark_min"] <= j["benchmark_max"]
    assert "severity" in j
    assert "summary_en" in j and "summary_th" in j

def test_analyze_window_mismatch():
    payload = {"kpi":"CTR", "window":3, "values":[0.01,0.012,0.011,0.013]}
    r = client.post("/analyze", json=payload)
    assert r.status_code == 400
