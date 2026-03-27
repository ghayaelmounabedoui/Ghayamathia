# EduPortal – Plateforme éducative avec chatbot intelligent

## Présentation

EduPortal est une plateforme éducative intégrant un assistant intelligent permettant d’accompagner les étudiants dans leur apprentissage.

Le chatbot repose sur une approche combinant :

* la recherche d’information dans des documents (PDF)
* la génération de réponses via un modèle d’intelligence artificielle

L’objectif est de proposer des réponses pertinentes, contextualisées et naturelles.

---

## Fonctionnalités

* Recherche d’information à partir de documents pédagogiques
* Génération de réponses intelligentes
* Interface de chat simple et intuitive
* Gestion des utilisateurs (enseignant / étudiant)
* Gestion des annonces

---

## Fonctionnement du chatbot

Le système suit une logique simple :

1. Recherche dans les documents disponibles
2. Si une information pertinente est trouvée → utilisation du contexte
3. Sinon → génération de réponse via le modèle

Ce mécanisme permet de limiter les réponses approximatives et d’améliorer la pertinence globale.

---

## Technologies utilisées

* Python
* FastAPI
* Mistral AI
* SQLAlchemy
* HTML / CSS

---

## Structure du projet

```bash
app/
 ├── main.py
 ├── rag/
 │    └── chatbot.py
 ├── templates/
 ├── static/
 └── data/
```

---

## Installation

```bash
git clone https://github.com/ghayaelmounabedoui/Ghayamathia.git
cd Ghayamathia

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Configuration

Créer un fichier `.env` :

```bash
MISTRAL_API_KEY=your_api_key
```

---

## Lancement

```bash
python -m uvicorn app.main:app --reload --port 7000
```

Accès :
http://127.0.0.1:7000

---

## Perspectives

* Amélioration de la pertinence des réponses
* Ajout d’un système de mémoire conversationnelle
* Optimisation du moteur de recherche documentaire
* Déploiement cloud

---

## Auteur

Ghaya El Mouna Bedoui
Data Scientist / AI Engineer
