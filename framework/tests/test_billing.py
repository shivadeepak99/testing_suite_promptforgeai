import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --- Test Matrix ---

def test_tiers_endpoint():
    r = client.get("/api/v1/billing/tiers")
    assert r.status_code == 200
    assert "tiers" in r.json()
    assert any(t["id"] == "free" for t in r.json()["tiers"])

def test_entitlements_unauth():
    r = client.get("/api/v1/me/entitlements")
    assert r.status_code in (401, 403)

# More tests would require fixtures/mocks for auth, DB, and webhooks.
# Example stubs for further expansion:

def test_purchase_checkout_url(monkeypatch):
    # Simulate a logged-in user and patch DB
    pass

def test_webhook_idempotency(monkeypatch):
    # Simulate webhook event, ensure no double grant
    pass

def test_atomic_debit(monkeypatch):
    # Simulate two concurrent paid calls, only one should succeed if balance < 2
    pass

# ... Add more tests for all matrix cases as needed ...
