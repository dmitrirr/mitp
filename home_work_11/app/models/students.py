from pydantic import BaseModel


class StudentCreate(BaseModel):
    last_name: str
    first_name: str
    faculty: str
    course: str
    grade: int


class StudentUpdate(BaseModel):
    last_name: str | None = None
    first_name: str | None = None
    faculty: str | None = None
    course: str | None = None
    grade: int | None = None


class StudentResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    faculty: str
    course: str
    grade: int

    class Config:
        from_attributes = True
