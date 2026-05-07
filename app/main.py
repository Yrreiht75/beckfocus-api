from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import leads, auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import leads, auth, dashboard

app = FastAPI(
    title="BeckFocus API",
    description="API de gestion de leads mariage",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://beckfocus.fr", "https://www.beckfocus.fr"],
    allow_methods=["POST", "GET", "PATCH"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(leads.router, prefix="/leads", tags=["leads"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

@app.get("/")
def root():
    return {"message": "BeckFocus API is running 🚀"}