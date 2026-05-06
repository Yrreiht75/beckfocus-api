from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api_is_running():
    """Vérifie que l'API tourne"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "BeckFocus API is running 🚀"}


def test_get_leads():
    """Vérifie que la route GET /leads répond"""
    response = client.get("/leads/")
    assert response.status_code == 200
    assert "leads" in response.json()


def test_lead_email_invalide():
    """Vérifie qu'un email invalide est rejeté"""
    response = client.post("/leads/", json={
        "nom": "Test",
        "email": "pasunemail",
        "message": "Test"
    })
    assert response.status_code == 422


def test_lead_sans_message():
    """Vérifie qu'un lead sans message est rejeté"""
    response = client.post("/leads/", json={
        "nom": "Test",
        "email": "test@test.com"
    })
    assert response.status_code == 422