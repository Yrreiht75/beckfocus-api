from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import leads

app = FastAPI(
    title="BeckFocus API",
    description="API de gestion de leads mariage",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://beckfocus.fr", "https://www.beckfocus.fr"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

app.include_router(leads.router, prefix="/leads", tags=["leads"])

@app.get("/")
def root():
    return {"message": "BeckFocus API is running 🚀"}