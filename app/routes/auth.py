from fastapi import APIRouter, HTTPException, Response, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.services.auth_service import authenticate_user, create_access_token

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


class LoginForm(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(form: LoginForm, response: Response):
    """Connexion admin — retourne un JWT dans un cookie"""
    if not authenticate_user(form.username, form.password):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    token = create_access_token(data={"sub": form.username})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 8
    )
    return {"message": "Connexion réussie ✅"}


@router.post("/logout")
def logout(response: Response):
    """Déconnexion — supprime le cookie JWT"""
    response.delete_cookie("access_token")
    return {"message": "Déconnexion réussie"}


@router.post("/login-form")
def login_form(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    """Connexion depuis le formulaire HTML"""
    if not authenticate_user(username, password):
        return templates.TemplateResponse(
    request=request,
    name="login.html",
    context={"error": "Identifiants incorrects"},
    status_code=401
)

    token = create_access_token(data={"sub": username})
    response = RedirectResponse(url="/dashboard/", status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 8
    )
    return response