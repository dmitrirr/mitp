from pathlib import Path

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.repository.students import StudentRepository
from app.repository.users import UserRepository
from app.service.auth import AuthService
from app.service.students import StudentsService

_db_path = Path(__file__).parent.parent / "students.db"
_engine = create_engine(f"sqlite:///{_db_path}")
_SessionLocal = sessionmaker(bind=_engine)

security = HTTPBearer()


def get_db_session() -> Session:
    return _SessionLocal()


def get_students_repository() -> StudentRepository:
    session = get_db_session()
    return StudentRepository(session)


def get_students_service() -> StudentsService:
    repository = get_students_repository()
    return StudentsService(repository)


def get_users_repository() -> UserRepository:
    session = get_db_session()
    return UserRepository(session)


def get_auth_service() -> AuthService:
    repository = get_users_repository()
    return AuthService(repository)


def get_current_user_email(
    credentials: HTTPAuthorizationCredentials = Security(security),
    auth_service: AuthService = Depends(get_auth_service),
) -> str:
    try:
        email = auth_service.verify_token(credentials.credentials)
        return email
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

