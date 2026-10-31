from datetime import datetime

from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
    relationship
)


# =========================
# DATABASE CONFIGURATION
# =========================

DATABASE_URL = "sqlite:///career_mentor.db"

engine = create_engine(
    DATABASE_URL,
    echo=False
)


# =========================
# BASE CLASS
# =========================

class Base(DeclarativeBase):
    pass


# =========================
# INTERVIEW MODEL
# =========================

class Interview(Base):

    __tablename__ = "interviews"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    candidate_name: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    experience: Mapped[int] = mapped_column(Integer)
    level: Mapped[str] = mapped_column(String)
    difficulty: Mapped[str] = mapped_column(String)
    overall_score: Mapped[float] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    questions: Mapped[list["Question"]] = relationship(
        back_populates="interview",
        cascade="all, delete-orphan"
    )


# =========================
# QUESTION MODEL
# =========================

class Question(Base):

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    interview_id: Mapped[int] = mapped_column(
        ForeignKey("interviews.id")
    )

    question_number: Mapped[int] = mapped_column(
        Integer
    )

    question_text: Mapped[str] = mapped_column(
        Text
    )

    interview: Mapped["Interview"] = relationship(
        back_populates="questions"
    )

    answer: Mapped["Answer"] = relationship(
        back_populates="question",
        uselist=False,
        cascade="all, delete-orphan"
    )


# =========================
# ANSWER MODEL
# =========================

class Answer(Base):

    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id")
    )

    answer_text: Mapped[str] = mapped_column(
        Text
    )

    score: Mapped[int] = mapped_column(
        Integer
    )

    technical_correctness: Mapped[int] = mapped_column(
        Integer
    )

    relevance: Mapped[int] = mapped_column(
        Integer
    )

    completeness: Mapped[int] = mapped_column(
        Integer
    )

    strengths: Mapped[str] = mapped_column(
        Text
    )

    improvements: Mapped[str] = mapped_column(
        Text
    )

    better_answer: Mapped[str] = mapped_column(
        Text
    )

    question: Mapped["Question"] = relationship(
        back_populates="answer"
    )


# =========================
# DATABASE SESSION
# =========================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# =========================
# CREATE TABLES
# =========================

Base.metadata.create_all(engine)

print("Database and tables created successfully!")