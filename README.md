# EduPortal – Plateforme éducative avec assistant intelligent

## Présentation

EduPortal est une plateforme éducative développée pour accompagner les élèves dans leur apprentissage, en combinant des ressources pédagogiques et un assistant intelligent.

Ce projet s’inscrit directement dans mon expérience en tant que tutrice en mathématiques chez Complétude, où j’ai pu observer les difficultés récurrentes des élèves : manque d’autonomie, incompréhension des notions, et besoin d’un accompagnement continu en dehors des séances.

L’objectif d’EduPortal est donc de proposer un outil capable de prolonger cet accompagnement de manière autonome, accessible à tout moment.

---

## Idée du projet

L’idée principale est de créer un assistant capable de répondre aux questions des élèves en s’appuyant sur :

* des documents pédagogiques (cours, exercices, explications)
* un modèle d’intelligence artificielle capable de compléter les réponses

Cela permet de simuler un encadrement proche de celui d’un tutorat, tout en restant disponible 24h/24.

---

## Fonctionnalités

* Recherche d’information à partir de documents pédagogiques
* Génération de réponses claires et adaptées au niveau de l’élève
* Interface de discussion simple et intuitive
* Gestion des utilisateurs (enseignants / étudiants)
* Publication d’annonces pédagogiques

---

## Fonctionnement du chatbot

Le chatbot repose sur une logique hybride :

1. Recherche dans les documents disponibles
2. Si une information pertinente est trouvée → utilisation du contexte
3. Sinon → génération d’une réponse via le modèle d’IA

Ce fonctionnement permet de garantir des réponses à la fois fiables et complètes.

---

## Apport par rapport à Complétude

Ce projet constitue une extension directe de mon activité de tutrice :

* Il permet de prolonger l’accompagnement entre les séances
* Il répond aux questions immédiates des élèves sans attendre
* Il favorise l’autonomie dans l’apprentissage
* Il reproduit une logique pédagogique basée sur l’explication et non uniquement la réponse

Ainsi, EduPortal agit comme un support complémentaire au tutorat traditionnel.

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

* Adaptation du niveau de réponse selon l’élève
* Ajout d’un suivi personnalisé
* Intégration d’exercices interactifs
* Amélioration du moteur de recherche documentaire

---

## Auteur

Ghaya El Mouna Bedoui
Data Scientist / AI Engineer
