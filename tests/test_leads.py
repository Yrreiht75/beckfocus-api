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

        # Vérifie que send a été appelé
        assert mock_send.called

        # Récupère les paramètres envoyés
        params = mock_send.call_args[0][0]

        # Vérifie que l'email contient le bouton
        assert "Répondre au client" in params["html"]
        assert "mailto:test@test.com" in params["html"]
        assert "contact@beckfocus.fr" in params["to"]