from datetime import date

from pydantic import BaseModel, EmailStr, Field, field_validator

CYRILLIC_ONLY_REGEX = r"^[а-яА-ЯёЁ\s]+$"


class AppealRequest(BaseModel):
    surname: str = Field(
        ...,
        pattern=CYRILLIC_ONLY_REGEX,
    )
    name: str = Field(
        ...,
        pattern=CYRILLIC_ONLY_REGEX,
    )
    date_of_birth: date
    phone_number: str = Field(..., min_length=12, max_length=12)
    email: EmailStr

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
        if not v.startswith("+7"):
            raise ValueError("phone number must start with +7")
        if not v[2:].isdigit():
            raise ValueError("phone number must have 10 digits after +7")
        return v
