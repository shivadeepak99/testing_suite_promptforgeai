
import pytest
from fastapi.testclient import TestClient
from demon_engine.api import pfcl_parser
from fastapi import FastAPI

app = FastAPI()
app.include_router(pfcl_parser.router)
client = TestClient(app)

def test_explain_fields():
    req = {
        "text": "Write a function to add two numbers.",
        "mode": "pro",
        "client": "vscode",
        "intent": "editor",
        "meta": {},
        "explain": True
    }
    response = client.post("/v2/upgrade", json=req)
    assert response.status_code == 200
    data = response.json()
    assert data["plan"] is not None
    assert data["fidelity_score"] is not None
    assert data["matched_entries"] is not None
    assert "Output contract" in data["message"]
