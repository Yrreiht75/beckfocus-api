from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models.lead import LeadCreate
from app.services import supabase_service
from app.services.supabase_service import save_lead, get_all_leads
from app.services.ia_service import generer_reponse_email
from app.services.email_service import envoyer_brouillon_email
from app.dependencies import get_current_user

router = APIRouter()


class StatutUpdate(BaseModel):
    statut: str


@router.post("/")
async def create_lead(lead: LeadCreate):
    """Reçoit une nouvelle demande — public"""
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
async def get_leads(current_user: str = Depends(get_current_user)):
    """Retourne toutes les demandes — protégé JWT"""
    leads = get_all_leads()
    return {"leads": leads}


@router.patch("/{lead_id}/statut")
async def update_statut(
    lead_id: int,
    update: StatutUpdate,
    current_user: str = Depends(get_current_user)
):
    """Met à jour le statut d'un lead — protégé JWT"""
    statuts_valides = ["nouveau", "en cours", "répondu", "converti", "annulé"]

    if update.statut not in statuts_valides:
        raise HTTPException(
            status_code=400,
            detail=f"Statut invalide. Valeurs acceptées : {statuts_valides}"
        )

    result = supabase_service.update_lead_statut(lead_id, update.statut)
    return {"message": "Statut mis à jour ✅", "lead": result}
