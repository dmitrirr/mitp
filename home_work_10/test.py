from pathlib import Path

import httpx
import pytest
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

from models import Base, StudentGrade

BASE_URL = "http://localhost:8000"
DB_PATH = Path(__file__).parent / "students.db"


@pytest.fixture(autouse=True)
def clear_table():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        stmt = delete(StudentGrade)
        session.execute(stmt)
        session.commit()
    yield


@pytest.fixture
def client():
    return httpx.Client(base_url=BASE_URL)


def test_crud_flow(client):
    response = client.get("/students/")
    assert response.status_code == 200
    assert response.json() == []

    create_data = {
        "last_name": "Ivanov",
        "first_name": "Ivan",
        "faculty": "АВТФ",
        "course": "Мат. Анализ",
        "grade": 85,
    }
    response = client.post("/students/", json=create_data)
    assert response.status_code == 200
    created = response.json()
    student_id = created["id"]
    assert created == {
        "id": student_id,
        "last_name": "Ivanov",
        "first_name": "Ivan",
        "faculty": "АВТФ",
        "course": "Мат. Анализ",
        "grade": 85,
    }

    response = client.get("/students/")
    assert response.status_code == 200
    students = response.json()
    assert students == [
        {
            "id": student_id,
            "last_name": "Ivanov",
            "first_name": "Ivan",
            "faculty": "АВТФ",
            "course": "Мат. Анализ",
            "grade": 85,
        }
    ]

    update_data = {
        "last_name": "Petrov",
        "grade": 90,
    }
    response = client.put(f"/students/{student_id}", json=update_data)
    assert response.status_code == 200
    updated = response.json()
    assert updated == {
        "id": student_id,
        "last_name": "Petrov",
        "first_name": "Ivan",
        "faculty": "АВТФ",
        "course": "Мат. Анализ",
        "grade": 90,
    }

    response = client.get("/students/")
    assert response.status_code == 200
    students = response.json()
    assert students == [
        {
            "id": student_id,
            "last_name": "Petrov",
            "first_name": "Ivan",
            "faculty": "АВТФ",
            "course": "Мат. Анализ",
            "grade": 90,
        }
    ]

    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Student deleted successfully"}

    response = client.get("/students/")
    assert response.status_code == 200
    assert response.json() == []
