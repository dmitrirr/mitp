from typing import List

from ..models.students import StudentCreate, StudentResponse, StudentUpdate
from repository import StudentRepository
from models import StudentGrade


class StudentsService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def create_student(self, student: StudentCreate) -> StudentResponse:
        student_grade = StudentGrade(
            last_name=student.last_name,
            first_name=student.first_name,
            faculty=student.faculty,
            course=student.course,
            grade=student.grade,
        )
        self.repository.insert([student_grade])
        return StudentResponse.model_validate(student_grade)

    def get_students(self) -> List[StudentResponse]:
        students = self.repository.select()
        return [StudentResponse.model_validate(s) for s in students]

    def update_student(self, id: int, student: StudentUpdate) -> StudentResponse:
        updated = self.repository.update_by_id(
            id=id,
            last_name=student.last_name,
            first_name=student.first_name,
            faculty=student.faculty,
            course=student.course,
            grade=student.grade,
        )
        return StudentResponse.model_validate(updated)

    def delete_student(self, id: int) -> None:
        self.repository.delete_by_id(id)

