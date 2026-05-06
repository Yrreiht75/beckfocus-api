# BeckFocus API 🎥

API de gestion de leads mariage pour BeckFocus Production.  
Permet de recevoir les demandes du site, de les stocker et de générer automatiquement un brouillon d'email de réponse grâce à l'IA.

## Stack technique

- **FastAPI** — Framework API Python
- **Supabase** — Base de données PostgreSQL
- **Groq / LLaMA 3.3** — Génération de réponses IA
- **Pytest** — Tests automatisés

## Fonctionnalités

- Réception des demandes depuis le formulaire beckfocus.fr
- Validation automatique des données
- Sauvegarde en base de données
- Génération d'un email de réponse personnalisé par IA selon la formule choisie
- Tests automatisés

## Installation

### Prérequis
- Python 3.11+
- Un compte Supabase
- Une clé API Groq

### Lancer le projet

```bash
git clone https://github.com/Yrreiht75/beckfocus-api.git
cd beckfocus-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Variables d'environnement

Crée un fichier `.env` à partir de `.env.example` :

```bash
cp .env.example .env
```

Remplis les valeurs dans `.env` :
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GROQ_API_KEY=your_groq_key

### Démarrer l'API

```bash
uvicorn app.main:app --reload
```

L'API tourne sur `http://127.0.0.1:8000`  
Documentation interactive : `http://127.0.0.1:8000/docs`

## Tests

```bash
pytest tests/ -v
```

## Roadmap

- [ ] Envoi du brouillon par email via Resend
- [ ] Dockerisation
- [ ] Pipeline CI/CD Jenkins
- [ ] Déploiement Kubernetes