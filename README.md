Voici le README complet et documenté. Remplace tout le contenu de README.md :
markdown

# BeckFocus API 🎥

API de gestion de leads mariage pour **BeckFocus Production**, studio de photographie et vidéographie basé à Paris et Île-de-France.

[![CI/CD](https://github.com/Yrreiht75/beckfocus-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Yrreiht75/beckfocus-api/actions)

---

## 🎯 Contexte et problème résolu

BeckFocus Production reçoit des demandes de clients via plusieurs canaux (formulaire web, Instagram DM). Avant ce projet, chaque demande nécessitait une réponse manuelle : lire le message, comprendre le besoin, rédiger un email personnalisé, proposer la bonne formule.

**Ce projet automatise ce flux :**
- Les demandes sont centralisées dans une base de données
- L'IA analyse chaque demande et génère un brouillon de réponse personnalisé
- Le photographe reçoit le brouillon par email et n'a plus qu'à valider et envoyer
- Un dashboard permet de suivre et gérer tous les leads

---

## 🌐 Production

| Service | URL |
|---------|-----|
| API.    | https://api.beckfocus.fr |
| Documentation interactive | https://api.beckfocus.fr/docs |
| Dashboard admin | https://api.beckfocus.fr/dashboard |

---

## 🔄 Flux complet d'une demande client

1. Le client remplit le formulaire sur **beckfocus.fr** ou envoie un DM Instagram
2. Le Worker Cloudflare envoie les emails de notification et confirmation
3. L'API reçoit la demande et la sauvegarde dans Supabase
4. La formule choisie est récupérée depuis la base de données (tarifs inclus)
5. L'IA Groq génère un email de réponse personnalisé
6. Le brouillon est envoyé sur contact@beckfocus.fr avec un bouton **"Répondre au client"**
7. Le photographe valide, modifie si besoin, et envoie
8. Le statut est mis à jour dans le dashboard


---

## 🏗️ Architecture

**Canaux d'entrée**
- beckfocus.fr → Cloudflare Worker → API
- Instagram DM → Meta Webhook → API

**API (FastAPI / Railway)**
- Validation des données (Pydantic)
- Authentification JWT
- Orchestration des services

**Services**
- Supabase → stockage des leads et formules
- Groq LLaMA → génération des emails IA
- Resend → envoi des emails

## 🛠️ Stack technique et décisions

### FastAPI (Python)
Choisi pour sa rapidité de développement, sa validation automatique des données avec Pydantic, et sa documentation Swagger auto-générée. Alternative à Flask mais plus moderne et performant.

### Supabase (PostgreSQL)
Base de données hébergée avec API REST auto-générée. Choisi pour le free tier généreux et la simplicité d'intégration avec Python. Les formules et tarifs sont stockés en base (pas dans le code) pour éviter de les exposer sur GitHub.

### Groq / LLaMA 3.3 70B
IA open source hébergée sur les serveurs Groq. Choisi pour la gratuité et la rapidité. Alternative à OpenAI GPT-4 sans carte bancaire requise. Le prompt inclut le contexte complet des formules pour des réponses précises.

### Resend
Service d'envoi d'emails moderne avec API simple. Choisi pour son free tier (3000 emails/mois) et sa compatibilité avec le domaine beckfocus.fr déjà vérifié.

### JWT + Argon2
Authentification par token JWT stocké dans un cookie `httponly` (plus sécurisé que localStorage). Argon2 pour le hachage des mots de passe (plus moderne que bcrypt).

### Docker
Containerisation pour garantir le même comportement en local et en production. L'image Python 3.11-slim est utilisée pour réduire la taille.

### GitHub Actions
Pipeline CI/CD déclenché à chaque `git push`. Choisi plutôt que Jenkins pour sa simplicité, sa gratuité et son intégration native avec GitHub. Les secrets sont stockés dans GitHub Secrets, jamais dans le code.

### Railway
Hébergement de l'API avec déploiement automatique depuis GitHub. Choisi pour le free tier et la simplicité de configuration.

---

## 🔐 Sécurité

- **Variables sensibles** : jamais dans le code, toujours dans `.env` (local) ou GitHub Secrets / Railway Variables (production)
- **Mots de passe** : hachés avec Argon2 au démarrage, jamais stockés en clair
- **JWT** : stocké en cookie `httponly` — inaccessible depuis JavaScript
- **Webhook Meta** : signature HMAC-SHA256 vérifiée à chaque requête
- **Supabase RLS** : Row Level Security activé sur toutes les tables
- **Formules et tarifs** : stockés en base de données, invisibles sur GitHub

---

## 📦 Structure du projet

beckfocus-api/
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline CI/CD GitHub Actions
├── app/
│   ├── main.py             # Configuration FastAPI + middlewares
│   ├── dependencies.py     # Vérification JWT (Depends)
│   ├── models/
│   │   └── lead.py         # Modèles Pydantic (validation)
│   ├── routes/
│   │   ├── leads.py        # Endpoints leads
│   │   ├── auth.py         # Endpoints authentification
│   │   ├── dashboard.py    # Dashboard HTML
│   │   └── webhooks.py     # Webhook Instagram
│   ├── services/
│   │   ├── supabase_service.py  # CRUD base de données
│   │   ├── ia_service.py        # Génération IA (Groq)
│   │   ├── email_service.py     # Envoi emails (Resend)
│   │   └── auth_service.py      # JWT + hachage
│   └── templates/
│       ├── login.html      # Page de connexion
│       └── dashboard.html  # Dashboard leads
├── tests/
│   └── test_leads.py       # Tests unitaires (pytest)
├── Dockerfile              # Image Docker
├── docker-compose.yml      # Orchestration locale
├── requirements.txt        # Dépendances Python
├── .env.example            # Template variables d'environnement
└── README.md


---

## 🚀 Installation

### Prérequis
- Python 3.11+
- Docker
- Comptes : Supabase, Groq, Resend

### Lancer en local

```bash
git clone https://github.com/Yrreiht75/beckfocus-api.git
cd beckfocus-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Remplis les variables dans .env
uvicorn app.main:app --reload
```

### Lancer avec Docker

```bash
docker build -t beckfocus-api .
docker run --env-file .env -p 8000:8000 beckfocus-api
```

---

## ⚙️ Variables d'environnement

```bash
# Base de données
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# IA
GROQ_API_KEY=your_groq_key

# Emails
RESEND_API_KEY=your_resend_key

# Authentification
SECRET_KEY=your_jwt_secret_key
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_password

# Meta / Instagram
META_VERIFY_TOKEN=your_webhook_token
META_APP_SECRET=your_meta_app_secret
```

---

## 📡 Endpoints

| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| GET | `/` | Statut de l'API | Public |
| POST | `/leads/` | Créer un lead | Public |
| GET | `/leads/` | Lister les leads | JWT |
| PATCH | `/leads/{id}/statut` | Modifier le statut | JWT |
| POST | `/auth/login` | Connexion API | Public |
| POST | `/auth/login-form` | Connexion dashboard | Public |
| POST | `/auth/logout` | Déconnexion | JWT |
| GET | `/dashboard/` | Dashboard leads | JWT |
| GET | `/dashboard/login` | Page de connexion | Public |
| GET | `/webhooks/instagram` | Vérification webhook | Meta |
| POST | `/webhooks/instagram` | Réception DM Instagram | Meta |

---

## 🧪 Tests

```bash
pytest tests/ -v
```

Les tests utilisent des **mocks** pour simuler les services externes (Supabase, Resend) — les tests unitaires ne dépendent pas de services tiers.

| Test | Ce qu'il vérifie |
|------|-----------------|
| `test_api_is_running` | L'API démarre correctement |
| `test_lead_email_invalide` | Pydantic rejette un email invalide |
| `test_lead_sans_message` | Pydantic rejette un lead incomplet |
| `test_email_contient_bouton_repondre` | L'email contient le bouton mailto |
| `test_login_succes` | L'authentification JWT fonctionne |
| `test_login_mauvais_password` | Un mauvais mot de passe est rejeté |
| `test_login_mauvais_username` | Un mauvais username est rejeté |
| `test_get_leads_sans_token` | La route est protégée sans token |
| `test_get_leads_avec_token` | La route est accessible avec JWT |

---

## 🔄 CI/CD

Chaque `git push` sur `main` déclenche automatiquement :

git push → GitHub Actions
↓
Tests pytest (9 tests)
↓ si OK
Build image Docker
↓ si OK
Railway redéploie automatiquement


---

## 📋 Roadmap

- [x] API REST CRUD leads
- [x] Validation données (Pydantic)
- [x] Base de données Supabase
- [x] Génération IA (Groq / LLaMA)
- [x] Envoi emails (Resend)
- [x] Bouton répondre au client (mailto)
- [x] Authentification JWT
- [x] Dashboard de gestion des leads
- [x] Webhook Instagram (Meta API)
- [x] Containerisation Docker
- [x] Pipeline CI/CD GitHub Actions
- [x] Déploiement Railway
- [x] Domaine custom api.beckfocus.fr
- [ ] Dashboard React (en développement)
- [ ] Connexion compte Instagram BeckFocus (en cours)
- [ ] Intégration WhatsApp Business
- [ ] Jenkins + Kubernetes (roadmap DevOps)

---

## 👨‍💻 Auteur

**Thierry Nicolas** — Développeur Backend Python  
Projet réel en production sur [beckfocus.fr](https://beckfocus.fr)