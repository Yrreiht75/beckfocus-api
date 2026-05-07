import os
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
from app.services.email_service import envoyer_brouillon_email

client = TestClient(app)


def test_api_is_running():
    """Vérifie que l'API tourne"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "BeckFocus API is running 🚀"}


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


def test_email_contient_bouton_repondre():
    """Vérifie que l'email brouillon contient le bouton répondre"""
    lead = {
        "nom": "Test Client",
        "email": "test@test.com",
        "telephone": "0612345678",
        "date_evenement": "2027-06-15",
        "formule": "Signature",
        "message": "Test message"
    }
    reponse_ia = "Bonjour, voici notre réponse."

    with patch("app.services.email_service.resend.Emails.send") as mock_send:
        mock_send.return_value = {"id": "test-id"}
        envoyer_brouillon_email(lead, reponse_ia)
        assert mock_send.called
        params = mock_send.call_args[0][0]
        assert "Répondre au client" in params["html"]
        assert "mailto:test@test.com" in params["html"]
        assert "contact@beckfocus.fr" in params["to"]


def test_login_succes():
    """Vérifie qu'on peut se connecter avec les bons identifiants"""
    response = client.post("/auth/login", json={
        "username": "beck",
        "password": os.getenv("ADMIN_PASSWORD")
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Connexion réussie ✅"
    assert "access_token" in response.cookies


def test_login_mauvais_password():
    """Vérifie qu'un mauvais mot de passe est rejeté"""
    response = client.post("/auth/login", json={
        "username": "beck",
        "password": "mauvais_password"
    })
    assert response.status_code == 401


def test_login_mauvais_username():
    """Vérifie qu'un mauvais username est rejeté"""
    response = client.post("/auth/login", json={
        "username": "hacker",
        "password": "nimportequoi"
    })
    assert response.status_code == 401


def test_get_leads_sans_token():
    """Vérifie que GET /leads est protégé sans token"""
    response = client.get("/leads/")
    assert response.status_code == 401


def test_get_leads_avec_token():
    """Vérifie que GET /leads est accessible avec un token valide"""
    from app.services.auth_service import create_access_token

    # Crée un token directement sans passer par le login
    token = create_access_token(data={"sub": "beck"})

    with TestClient(app) as persistent_client:
        # Injecte le cookie manuellement
        persistent_client.cookies.set("access_token", token)

        response = persistent_client.get("/leads/")
        assert response.status_code == 200
        assert "leads" in response.json()