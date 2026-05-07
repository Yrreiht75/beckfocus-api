import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def save_lead(lead_data: dict):
    response = supabase.table("leads").insert(lead_data).execute()
    return response.data

def get_all_leads():
    response = supabase.table("leads").select("*").execute()
    return response.data

def update_lead_statut(lead_id: int, statut: str):
    response = supabase.table("leads").update(
        {"statut": statut}
    ).eq("id", lead_id).execute()
    return response.data