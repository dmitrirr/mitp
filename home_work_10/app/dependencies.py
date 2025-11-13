from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from repository import StudentRepository
from app.service.students import StudentsService

_db_path = Path(__file__).parent.parent / "students.db"
_engine = create_engine(f"sqlite:///{_db_path}")
_SessionLocal = sessionmaker(bind=_engine)


def get_db_session() -> Session:
    return _SessionLocal()


def get_students_repository() -> StudentRepository:
    session = get_db_session()
    return StudentRepository(session)


def get_students_service() -> StudentsService:
    repository = get_students_repository()
    return StudentsService(repository)

