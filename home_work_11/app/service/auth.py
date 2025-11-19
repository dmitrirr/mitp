import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from app.repository.users import UserRepository

JWT_SECRET_KEY = secrets.token_urlsafe(32)
JWT_ALGORITHM = "HS256"


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, email: str, password: str) -> str:
        existing_user = self.repository.get_user_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        self.repository.create_user(email, password_hash)
        return self._generate_token(email)

    def login(self, email: str, password: str) -> str:
        user = self.repository.get_user_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            raise ValueError("Invalid email or password")

        return self._generate_token(email)

    def _generate_token(self, email: str) -> str:
        payload = {
            "email": email,
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    def verify_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            email = payload.get("email")
            if email is None:
                raise ValueError("Invalid token")
            return email
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.JWTError:
            raise ValueError("Invalid token")

