# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_ok_green():
    payload = {"kpi":"CTR","window":5,"values":[1,1,1,1,1],"role":"anon"}
    r = client.post("/analyze", json=payload)
    assert r.status_code == 200
    assert r.json()["severity"] == "Green"

def test_invalid_length():
    payload = {"kpi":"CTR","window":5,"values":[1,2],"role":"anon"}
    r = client.post("/analyze", json=payload)
    assert r.status_code == 400

def test_admin_masking():
    payload = {"kpi":"CTR","window":4,"values":[1,1,1,1],"role":"admin"}
    r = client.post("/analyze", json=payload)
    assert r.status_code == 200
