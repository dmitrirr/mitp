import json
from datetime import date
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field, field_validator

router = APIRouter()

CYRILLIC_ONLY_REGEX = r"^[а-яА-ЯёЁ\s]+$"


class AppealRequest(BaseModel):
    surname: str = Field(
        ...,
        description="Surname",
        pattern=CYRILLIC_ONLY_REGEX,
    )
    name: str = Field(
        ...,
        description="Name",
        pattern=CYRILLIC_ONLY_REGEX,
    )
    date_of_birth: date = Field(..., description="Date of birth")
    phone_number: str = Field(..., description="Phone number")
    email: EmailStr = Field(..., description="E-mail")

    @field_validator("surname")
    @classmethod
    def validate_surname(cls, v: str) -> str:
        if v and not v[0].isupper():
            raise ValueError("surname must start with a capital letter")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v and not v[0].isupper():
            raise ValueError("name must start with a capital letter")
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not v:
            raise ValueError("phone number cannot be empty")
        cleaned = v.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+", "")
        if not cleaned.isdigit():
            raise ValueError("phone number must contain only digits and allowed characters")
        return v


@router.post("/appeals/", tags=["appeals"])
async def create_appeal(appeal: AppealRequest):
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    appeal_data = appeal.model_dump()
    appeal_data["date_of_birth"] = appeal_data["date_of_birth"].isoformat()

    file_path = data_dir / "appeals.json"

    appeals = []
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            appeals = json.load(f)

    appeals.append(appeal_data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(appeals, f, ensure_ascii=False, indent=2)

    return {"message": "Appeal successfully saved", "appeal": appeal_data}

