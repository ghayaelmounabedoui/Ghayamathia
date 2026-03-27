from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base


# =========================
# USER
# =========================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    role = Column(String(20), default="student")
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    is_approved = Column(Boolean, default=False)

    # 🔥 IMPORTANT : préciser foreign_keys
    resources = relationship(
        "Resource",
        foreign_keys="Resource.created_by_id"
    )

    announcements = relationship(
        "Announcement",
        foreign_keys="Announcement.created_by_id"
    )
# =========================
# RESOURCE
# =========================

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)

    title = Column(String(150), nullable=False)
    category = Column(String(100))
    description = Column(Text)

    file_path = Column(String, nullable=True)

    target = Column(String, default="all")

    student_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔥 IMPORTANT ICI
    created_by = relationship(
        "User",
        foreign_keys=[created_by_id]
    )

    student = relationship(
        "User",
        foreign_keys=[student_id]
    )
# =========================
# ANNOUNCEMENT
# =========================

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)

    target = Column(String, default="all")
    student_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 🔥 IMPORTANT
    created_by = relationship(
        "User",
        foreign_keys=[created_by_id]
    )

    student = relationship(
        "User",
        foreign_keys=[student_id]
    )