from fastapi import APIRouter, HTTPException
from app.models.lead import LeadCreate
from app.services.supabase_service import save_lead, get_all_leads
from app.services.ia_service import generer_reponse_email

router = APIRouter()

@router.post("/")
async def create_lead(lead: LeadCreate):
    """Reçoit une nouvelle demande depuis le formulaire beckfocus.fr"""
    data = lead.model_dump()

    # Convertir la date en string pour Supabase
    if data.get("date_evenement"):
        data["date_evenement"] = str(data["date_evenement"])

    # Générer la réponse IA
    reponse_ia = generer_reponse_email(data)
    data["reponse_ia"] = reponse_ia

    # Sauvegarder en base avec la réponse IA
    result = save_lead(data)

    return {
        "message": "Lead reçu ✅",
        "lead": result,
        "reponse_ia": reponse_ia
    }

@router.get("/")
async def get_leads():
    """Retourne toutes les demandes"""
    leads = get_all_leads()
    return {"leads": leads}