from fastapi import FastAPI
from app.routes import leads

app = FastAPI(
    title="BeckFocus API",
    description="API de gestion de leads mariage",
    version="1.0.0"
)

app.include_router(leads.router, prefix="/leads", tags=["leads"])

@app.get("/")
def root():
    return {"message": "BeckFocus API is running 🚀"}