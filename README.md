# EduPortal Python Beautiful

Plateforme éducative 100% Python (FastAPI + Jinja2 + SQLite), prête à lancer.

## Fonctionnalités
- Inscription / connexion
- Sessions sécurisées via cookie signé
- Rôles `teacher` / `student`
- Dashboard enseignant élégant
- Dashboard étudiant élégant
- Ressources pédagogiques
- Annonces
- Profil utilisateur
- Base SQLite locale
- Seed de données de démonstration

## Lancement
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload --port 8000
```

Ensuite ouvre :
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## Comptes démo
- teacher / teacher123
- student / student123

## Notes
- Le mot de passe est hashé en PBKDF2 (stdlib Python)
- Aucun Node.js / React nécessaire
