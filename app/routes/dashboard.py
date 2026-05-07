from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.supabase_service import get_all_leads
from app.dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Page de connexion"""
    return templates.TemplateResponse(request=request, name="login.html")


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    """Dashboard principal — protégé JWT"""
    try:
        current_user = get_current_user(request)
    except:
        return RedirectResponse(url="/dashboard/login")

    leads = get_all_leads()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"leads": leads, "user": current_user}
    )