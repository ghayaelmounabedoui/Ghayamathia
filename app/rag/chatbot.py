from pathlib import Path
import os
import PyPDF2

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter
# =========================
# CONFIG
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "app" / "data"

client = None
documents = []


# =========================
# INIT
# =========================

def load_chatbot():
    global client, db

    # ✅ éviter rechargement
    if client is not None and db is not None:
        return db, client

    print("🔄 Initialisation Mistral...")

    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        raise ValueError("⚠️ MISTRAL_API_KEY non définie")

    client = MistralClient(api_key=api_key)

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    # =========================
    # 🔹 CAS 1 : pas de docs
    # =========================
    if not pdf_files:
        print("⚠️ Aucun PDF → mode LLM seul")
        db = None
        return db, client

    # =========================
    # 🔹 1. Extraction texte
    # =========================
    all_texts = []

    for pdf in pdf_files:
        try:
            with open(pdf, "rb") as f:
                reader = PyPDF2.PdfReader(f)

                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        all_texts.append(text)

        except Exception as e:
            print(f"Erreur PDF {pdf}:", e)

    print(f"✅ {len(all_texts)} pages chargées")

    # =========================
    # 🔹 2. Split texte
    # =========================
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    split_docs = splitter.create_documents(all_texts)

    # =========================
    # 🔹 3. Embeddings (gratuit)
    # =========================
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # =========================
    # 🔹 4. Vector DB
    # =========================
    db = FAISS.from_documents(split_docs, embeddings)

    print("✅ Vector DB créée")

    return db, client

# =========================
# LLM CALL (FIX)
# =========================

def ask_mistral(client, prompt):
    response = client.chat(
        model="mistral-tiny",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# =========================
# RAG SIMPLE
# =========================

def retrieve_context(question, documents):
    words = [w.lower() for w in question.split() if len(w) > 3]

    best_doc = None
    best_score = 0

    for doc in documents:
        doc_lower = doc.lower()
        score = sum(1 for w in words if w in doc_lower)

        if score > best_score:
            best_score = score
            best_doc = doc

    if best_score >= 2:
        return best_doc[:1200]

    return None


# =========================
# MAIN FUNCTION
# =========================

def ask_chatbot(question: str):
    global documents, client

    if client is None:
        load_chatbot()

    question = question.strip()

    if not question:
        return "Pose-moi une question 😊"

    # 🔍 RAG
    if documents:
        context = retrieve_context(question, documents)

        if context:
            prompt = f"""
Tu es GhayaBot.

Réponds en utilisant ce contexte :

{context}

Question :
{question}
"""
            response = ask_llm(prompt)

            if response:
                return response

    # 🤖 fallback
    response = ask_llm(f"""
Réponds clairement en français :

{question}
""")

    if response:
        return response

    return "Je suis là 😊 reformule ta question"