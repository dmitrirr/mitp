from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

from app.db.models import Base
from app.main import app

DB_PATH = Path(__file__).parent / "students.db"


@pytest.fixture(autouse=True)
def clear_tables():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(delete(table))
        session.commit()
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_token(client):
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
    }
    response = client.post("/register", json=register_data)
    assert response.status_code == 200
    return response.json()["token"]


@pytest.fixture
def authenticated_client(client, auth_token):
    client.headers["Authorization"] = f"Bearer {auth_token}"
    return client


def test_register(client):
    register_data = {
        "email": "test@example.com",
        "password": "password123",
    }
    response = client.post("/register", json=register_data)
    assert response.status_code == 200
    assert "token" in response.json()
    assert len(response.json()["token"]) > 0


def test_register_duplicate_email(client):
    register_data = {
        "email": "test@example.com",
        "password": "password123",
    }
    response = client.post("/register", json=register_data)
    assert response.status_code == 200

    response = client.post("/register", json=register_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_login(client):
    register_data = {
        "email": "test@example.com",
        "password": "mypassword",
    }
    response = client.post("/register", json=register_data)
    assert response.status_code == 200

    login_data = {
        "email": "test@example.com",
        "password": "mypassword",
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
    assert "token" in response.json()
    assert len(response.json()["token"]) > 0


def test_login_invalid_email(client):
    login_data = {
        "email": "nonexistent@example.com",
        "password": "password123",
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_login_invalid_password(client):
    register_data = {
        "email": "test@example.com",
        "password": "correctpassword",
    }
    response = client.post("/register", json=register_data)
    assert response.status_code == 200

    login_data = {
        "email": "test@example.com",
        "password": "wrongpassword",
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_protected_route_without_auth(client):
    response = client.get("/students/")
    assert response.status_code == 403


def test_protected_route_with_invalid_token(client):
    client.headers["Authorization"] = "Bearer invalid_token"
    response = client.get("/students/")
    assert response.status_code == 401


def test_crud_flow(authenticated_client):
    response = authenticated_client.get("/students/")
    assert response.status_code == 200
    assert response.json() == []

    create_data = {
        "last_name": "Ivanov",
        "first_name": "Ivan",
        "faculty": "АВТФ",
        "course": "Мат. Анализ",
        "grade": 85,
    }
    response = authenticated_client.post("/students/", json=create_data)
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

    response = authenticated_client.get("/students/")
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

    response = authenticated_client.get(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": student_id,
        "last_name": "Ivanov",
        "first_name": "Ivan",
        "faculty": "АВТФ",
        "course": "Мат. Анализ",
        "grade": 85,
    }

    update_data = {
        "last_name": "Petrov",
        "grade": 90,
    }
    response = authenticated_client.put(f"/students/{student_id}", json=update_data)
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

    response = authenticated_client.get("/students/")
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

    response = authenticated_client.delete(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Student deleted successfully"}

    response = authenticated_client.get("/students/")
    assert response.status_code == 200
    assert response.json() == []
