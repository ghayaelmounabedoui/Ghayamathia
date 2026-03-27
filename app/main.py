from pathlib import Path
import os
import shutil
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, Request, Depends, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from app.rag.chatbot import load_chatbot
from .database import Base, engine, get_db
from .models import User, Resource, Announcement
from .security import hash_password, verify_password
from app.rag.chatbot import ask_mistral

# =========================
# INIT
# =========================

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Static
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Uploads
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

Base.metadata.create_all(bind=engine)


# =========================
# HELPERS
# =========================

def current_user(request: Request, db: Session) -> Optional[User]:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


def require_teacher(request: Request, db: Session) -> User:
    user = current_user(request, db)
    if not user:
        raise HTTPException(status_code=401)
    if user.role != "teacher":
        raise HTTPException(status_code=403)
    return user


# =========================
# HOME
# =========================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# =========================
# REGISTER
# =========================

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    form = await request.form()

    user = User(
        first_name=form.get("first_name"),
        last_name=form.get("last_name"),
        username=form.get("username"),
        email=form.get("email"),
        password_hash=hash_password(form.get("password")),
        role=form.get("role"),
        is_approved=True
    )

    db.add(user)
    db.commit()

    return RedirectResponse("/login", status_code=302)


# =========================
# LOGIN
# =========================

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    form = await request.form()

    user = db.query(User).filter(User.email == form.get("email")).first()

    if not user or not verify_password(form.get("password"), user.password_hash):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Erreur login"})

    request.session["user_id"] = user.id
    return RedirectResponse("/dashboard", status_code=302)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")


# =========================
# DASHBOARD
# =========================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse("/login")

    counts = {
        "resources": db.query(Resource).count(),
        "announcements": db.query(Announcement).count(),
        "students": db.query(User).filter(User.role == "student").count(),
        "teachers": db.query(User).filter(User.role == "teacher").count(),
    }

    template = "teacher_dashboard.html" if user.role == "teacher" else "student_dashboard.html"

    return templates.TemplateResponse(
        template,
        {"request": request, "user": user, "counts": counts}
    )


# =========================
# RESOURCES
# =========================
@app.get("/about", response_class=HTMLResponse)
def about_page(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )
@app.get("/resources", response_class=HTMLResponse)
def resources_page(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse("/login")

    students = db.query(User).filter(User.role == "student").all()

    if user.role == "teacher":
        resources = db.query(Resource).all()
    else:
        resources = db.query(Resource).filter(
            (Resource.target == "all") |
            (Resource.student_id == user.id)
        ).all()

    return templates.TemplateResponse(
        "resources.html",
        {
            "request": request,
            "user": user,
            "resources": resources,
            "students": students
        }
    )


@app.post("/resources/add")
def add_resource(
    request: Request,
    title: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    target: str = Form(...),
    student_id: Optional[int] = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    user = require_teacher(request, db)

    filename = None

    if file and file.filename:
        filename = f"{int(datetime.utcnow().timestamp())}_{file.filename}"
        path = UPLOAD_DIR / filename

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    resource = Resource(
        title=title,
        category=category,
        description=description,
        target=target,
        student_id=student_id if target == "student" else None,
        file_path=filename,
        created_by_id=user.id
    )

    db.add(resource)
    db.commit()

    return RedirectResponse("/resources", status_code=302)


@app.post("/resources/delete/{resource_id}")
def delete_resource(
    resource_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user = require_teacher(request, db)

    resource = db.query(Resource).filter(Resource.id == resource_id).first()

    if not resource:
        return RedirectResponse("/resources", status_code=303)

    if resource.file_path:
        file_on_disk = UPLOAD_DIR / resource.file_path
        if file_on_disk.exists():
            file_on_disk.unlink()

    db.delete(resource)
    db.commit()

    return RedirectResponse("/resources", status_code=303)

@app.post("/resources/update/{id}")
def update_resource(
    id: int,
    title: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    target: str = Form(...),
    student_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    resource = db.query(Resource).filter(Resource.id == id).first()

    resource.title = title
    resource.category = category
    resource.description = description
    resource.target = target
    resource.student_id = student_id if target == "student" else None

    db.commit()

    return RedirectResponse("/resources", status_code=302)

qa_chain = load_chatbot()

class Question(BaseModel):
    question: str

@app.post("/chatbot")
def chat(q: Question):

    if qa_chain is None:
        return {"answer": "⚠️ Chatbot non disponible"}

    try:
        db, llm = qa_chain

        # 🔹 Si pas de DB → LLM direct
        if db is None:
            answer = ask_mistral(llm, q.question)
            return {"answer": answer, "source": "llm"}

        # 🔹 RAG
        docs = db.similarity_search(q.question, k=2)

        context = "\n".join([doc.page_content for doc in docs])

        if not context.strip():
            answer = ask_mistral(llm, q.question)
            return {"answer": answer, "source": "llm"}

        prompt = f"""
    Tu es un assistant intelligent et naturel.

RÈGLES :
- Réponds de façon courte (2-3 phrases max)
- Sois naturel comme une conversation
- Ne donne PAS trop d'informations d’un coup
- Réponds directement à la question
- Si c’est une salutation, réponds simplement


        CONTEXTE:
        {context}

        QUESTION:
        {q.question}
        """

        answer = ask_mistral(llm, prompt)

        return {"answer": answer, "source": "docs"}

    except Exception as e:
        print("❌ Chat error:", e)
        return {"answer": "⚠️ Erreur chatbot"}
@app.get("/chatbot", response_class=HTMLResponse)
def chatbot_page(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)

    if not user:
        return RedirectResponse("/login")

    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "user": user}
    )


# =========================
# ANNOUNCEMENTS
# =========================

@app.get("/announcements", response_class=HTMLResponse)
def announcements_page(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse("/login")

    announcements = db.query(Announcement).all()

    return templates.TemplateResponse(
        "announcements.html",
        {"request": request, "user": user, "announcements": announcements}
    )


@app.post("/announcements/add")
def add_announcement(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    user = require_teacher(request, db)

    announcement = Announcement(
        title=title,
        content=content,
        created_by_id=user.id
    )

    db.add(announcement)
    db.commit()

    return RedirectResponse("/announcements", status_code=302)


# =========================
# STUDENTS PAGE
# =========================

@app.get("/students", response_class=HTMLResponse)
def students_page(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)

    if not user:
        return RedirectResponse("/login")

    students = db.query(User).filter(User.role == "student").all()

    return templates.TemplateResponse(
        "students.html",
        {"request": request, "students": students}
    )