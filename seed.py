from app.database import Base, SessionLocal, engine
from app.models import Announcement, Resource, User
from app.security import hash_password

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

teacher = User(
    first_name="Aya",
    last_name="Professor",
    username="teacher",
    email="teacher@eduportal.local",
    password_hash=hash_password("teacher123"),
    role="teacher",
)
student = User(
    first_name="Ghaya",
    last_name="Student",
    username="student",
    email="student@eduportal.local",
    password_hash=hash_password("student123"),
    role="student",
)
db.add_all([teacher, student])
db.commit()
db.refresh(teacher)
db.refresh(student)

resources = [
    Resource(title="Algèbre — Fiche 1", category="Mathématiques", description="Équations, identités remarquables et exercices guidés.", created_by_id=teacher.id),
    Resource(title="Méthodologie dissertation", category="Français", description="Structure, plan détaillé et exemples d'introductions.", created_by_id=teacher.id),
    Resource(title="Physique — Forces", category="Sciences", description="Résumé visuel sur les lois de Newton.", created_by_id=teacher.id),
]
announcements = [
    Announcement(title="Bienvenue sur EduPortal", content="La plateforme est prête. Vous pouvez consulter les ressources et suivre les annonces ici.", created_by_id=teacher.id),
    Announcement(title="Nouveau support maths", content="Un nouveau support d'algèbre est disponible dans les ressources.", created_by_id=teacher.id),
]

db.add_all(resources + announcements)
db.commit()
db.close()

print("Seed terminé.")
