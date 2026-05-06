from fastapi import APIRouter, HTTPException
from app.models.lead import LeadCreate
from app.services.supabase_service import save_lead, get_all_leads
from app.services.ia_service import generer_reponse_email
from app.services.email_service import envoyer_brouillon_email

router = APIRouter()

@router.post("/")
async def create_lead(lead: LeadCreate):
    """Reçoit une nouvelle demande depuis le formulaire beckfocus.fr"""
    data = lead.model_dump()

    if data.get("date_evenement"):
        data["date_evenement"] = str(data["date_evenement"])

    reponse_ia = generer_reponse_email(data)
    data["reponse_ia"] = reponse_ia

    result = save_lead(data)

    envoyer_brouillon_email(data, reponse_ia)

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