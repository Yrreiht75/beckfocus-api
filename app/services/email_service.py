import os
import resend
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

def envoyer_brouillon_email(lead: dict, reponse_ia: str):
    try:
        mailto_body = quote(reponse_ia)
        mailto_subject = quote("Re: Votre demande BeckFocus Production")
        mailto_link = f"mailto:{lead.get('email')}?subject={mailto_subject}&body={mailto_body}"

        params = {
            "from": "BeckFocus Production <contact@beckfocus.fr>",
            "to": ["contact@beckfocus.fr"],
            "subject": f"📩 Nouvelle demande — {lead.get('nom')} | {lead.get('formule')} | {lead.get('date_evenement')}",
            "html": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333;">Nouvelle demande reçue</h2>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                    <tr><td style="padding: 8px; background: #f5f5f5;"><strong>Nom</strong></td><td style="padding: 8px;">{lead.get('nom')}</td></tr>
                    <tr><td style="padding: 8px; background: #f5f5f5;"><strong>Email</strong></td><td style="padding: 8px;">{lead.get('email')}</td></tr>
                    <tr><td style="padding: 8px; background: #f5f5f5;"><strong>Téléphone</strong></td><td style="padding: 8px;">{lead.get('telephone', 'Non renseigné')}</td></tr>
                    <tr><td style="padding: 8px; background: #f5f5f5;"><strong>Date</strong></td><td style="padding: 8px;">{lead.get('date_evenement', 'Non renseignée')}</td></tr>
                    <tr><td style="padding: 8px; background: #f5f5f5;"><strong>Formule</strong></td><td style="padding: 8px;">{lead.get('formule', 'Non renseignée')}</td></tr>
                    <tr><td style="padding: 8px; background: #f5f5f5;"><strong>Message</strong></td><td style="padding: 8px;">{lead.get('message')}</td></tr>
                </table>

                <h3 style="color: #333;">✉️ Brouillon de réponse généré par l'IA</h3>
                <div style="background: #f9f9f9; padding: 20px; border-left: 4px solid #d4a853; white-space: pre-line;">
                    {reponse_ia}
                </div>

                <a href="{mailto_link}"
                   style="display:inline-block;background:#d4a853;color:#000;padding:14px 28px;text-decoration:none;font-family:Arial,sans-serif;font-size:13px;font-weight:bold;margin-top:20px;border-radius:4px;">
                    ✉️ Répondre au client
                </a>

                <p style="color: #999; font-size: 12px; margin-top: 20px;">
                    Cliquez sur le bouton pour ouvrir votre boite mail avec la réponse pré-remplie.
                </p>
            </div>
            """
        }
        response = resend.Emails.send(params)
        print("✅ Email envoyé:", response)
        return response
    except Exception as e:
        print("❌ Erreur email:", e)
        return None