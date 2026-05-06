import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

FORMULES = {
    "Essentiel": """
        1 opérateur, de la cérémonie à la pièce montée, en photo ET vidéo.
        Tarif : 1 200€.
        Rendus : 200 photos retouchées + film d'environ 10 min.
        Options disponibles : drone (+100€), projection (+200€), frais de déplacement IDF (+50€ si trajets longs).
    """,
    "Signature": """
        2 opérateurs, des préparatifs à la pièce montée, en photo ET vidéo.
        Tarif : 1 500€. Présence du portraitiste offerte.
        Rendus : 600 photos retouchées + teaser + film 4K d'1 heure.
        Options disponibles : drone (+100€), projection (+200€), frais de déplacement IDF (+50€ si trajets longs).
    """,
    "Prestige": """
        Équipe complète : 1 vidéaste, 1 photographe, 2 portraitistes.
        Inclus : projection pendant la réception, toile des mariés, portraits des invités, drone offert.
        Tarif : 2 500€.
        Rendus : album photos 100 photos + 800 photos retouchées + teaser + film 4K d'1 heure + film sur clé USB.
        Options disponibles : frais de déplacement IDF (+50€ si trajets longs).
    """,
    "Sur mesure": """
        Formule entièrement personnalisée selon les besoins des mariés.
        Tarif et prestations à définir ensemble lors d'un premier échange.
        Options disponibles : drone (+100€), projection (+200€), frais de déplacement IDF (+50€ si trajets longs).
    """
}

def generer_reponse_email(lead: dict) -> str:
    """Génère un brouillon d'email de réponse pour un lead"""

    formule = lead.get('formule', 'non précisée')
    detail_formule = FORMULES.get(formule, "Formule à définir ensemble")

    prompt = f"""
    Tu es l'assistant de BeckFocus Production, photographe/vidéaste spécialisé mariages.
    
    Voici les formules disponibles :
    - Essentiel : {FORMULES['Essentiel']}
    - Signature : {FORMULES['Signature']}
    - Prestige : {FORMULES['Prestige']}
    - Sur mesure : {FORMULES['Sur mesure']}
    
    Nouvelle demande reçue :
    - Nom : {lead.get('nom')}
    - Email : {lead.get('email')}
    - Date du mariage : {lead.get('date_evenement', 'non précisée')}
    - Formule souhaitée : {formule} → {detail_formule}
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