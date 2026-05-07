import os
import hmac
import hashlib
from fastapi import APIRouter, Request, HTTPException, Query
from dotenv import load_dotenv
from app.services.supabase_service import save_lead
from app.services.ia_service import generer_reponse_email
from app.services.email_service import envoyer_brouillon_email

load_dotenv()

router = APIRouter()

VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")
APP_SECRET = os.getenv("META_APP_SECRET")

@router.get("/instagram")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    """Vérification du webhook par Meta"""
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        print("✅ Webhook Instagram vérifié")
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Token invalide")

@router.post("/instagram")
async def receive_instagram_message(request: Request):
    """Reçoit les DM Instagram"""
    body = await request.body()
    signature = request.headers.get("x-hub-signature-256", "")
    expected = "sha256=" + hmac.new(
        APP_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=403, detail="Signature invalide")

    data = await request.json()

    for entry in data.get("entry", []):
        for messaging in entry.get("messaging", []):
            sender_id = messaging.get("sender", {}).get("id")
            message_text = messaging.get("message", {}).get("text")

            if not message_text:
                continue

            lead_data = {
                "nom": f"Instagram {sender_id}",
                "email": f"instagram_{sender_id}@placeholder.com",
                "telephone": None,
                "date_evenement": None,
                "formule": "Sur mesure",
                "message": message_text,
                "statut": "nouveau"
            }

            reponse_ia = generer_reponse_email(lead_data)
            lead_data["reponse_ia"] = reponse_ia
            save_lead(lead_data)
            envoyer_brouillon_email(lead_data, reponse_ia)

    return {"status": "ok"}