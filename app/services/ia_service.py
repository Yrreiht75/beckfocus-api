import os
from groq import Groq
from dotenv import load_dotenv
from app.services.supabase_service import supabase

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_formules():
    """Récupère toutes les formules depuis Supabase"""
    response = supabase.table("formules").select("*").execute()
    return response.data

def get_formule(nom: str):
    """Récupère une formule spécifique depuis Supabase"""
    response = supabase.table("formules").select("*").eq("nom", nom).execute()
    if response.data:
        return response.data[0]
    return None

def generer_reponse_email(lead: dict) -> str:
    """Génère un brouillon d'email de réponse pour un lead"""

    formule_nom = lead.get('formule', 'non précisée')
    formule = get_formule(formule_nom)
    formules = get_formules()

    # Construit le contexte des formules pour l'IA
    contexte_formules = "\n".join([
        f"- {f['nom']} : {f['description']} | Tarif : {f['tarif']}€ | Rendus : {f['rendus']} | Options : {f['options']}"
        for f in formules
    ])

    # Détail de la formule choisie
    if formule:
        detail = f"{formule['description']} | Tarif : {formule['tarif']}€ | Rendus : {formule['rendus']}"
    else:
        detail = "Formule à définir ensemble"

    prompt = f"""
    Tu es l'assistant de BeckFocus Production, photographe/vidéaste spécialisé mariages.
    
    Voici les formules disponibles :
    {contexte_formules}
    
    Nouvelle demande reçue :
    - Nom : {lead.get('nom')}
    - Email : {lead.get('email')}
    - Date du mariage : {lead.get('date_evenement', 'non précisée')}
    - Formule souhaitée : {formule_nom} → {detail}
    - Message : {lead.get('message')}
    
    Rédige un email de réponse professionnel et chaleureux en français.
    L'email doit :
    - Remercier le client pour sa demande
    - Montrer que tu as compris ce qu'il recherche
    - Rappeler brièvement ce qu'inclut sa formule choisie avec les rendus
    - Mentionner le tarif de la formule choisie
    - Si le client mentionne un lieu éloigné, mentionner les frais de déplacement
    - Si le client parle de vidéo uniquement, lui rappeler que la formule inclut photo ET vidéo
    - Proposer un appel ou une rencontre pour discuter des détails
    - Ne jamais inventer d'autres tarifs que ceux fournis
    - Être signé "Beck, BeckFocus Production"
    
    Retourne uniquement le contenu de l'email, sans objet.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content