from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class LeadCreate(BaseModel):
    nom: str
    email: EmailStr
    telephone: Optional[str] = None
    date_evenement: Optional[date] = None
    formule: Optional[str] = None
    message: str

class LeadResponse(BaseModel):
    id: int
    nom: str
    email: str
    telephone: Optional[str] = None
    date_evenement: Optional[date] = None
    formule: Optional[str] = None
    message: str
    statut: str
    reponse_ia: Optional[str] = None