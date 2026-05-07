from fastapi import Request, HTTPException
from app.services.auth_service import verify_token

def get_current_user(request: Request) -> str:
    """Vérifie le token JWT depuis le cookie"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Non authentifié")
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    return username