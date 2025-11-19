import csv
from pathlib import Path
from typing import List

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.db.models import StudentGrade


class StudentRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert(self, items: List[StudentGrade]) -> None:
        self.session.add_all(items)
        self.session.commit()

    def select(self) -> List[StudentGrade]:
        stmt = select(StudentGrade)
        return list(self.session.scalars(stmt).all())

    def select_by_id(self, id: int) -> StudentGrade:
        student = self.session.get(StudentGrade, id)
        if student is None:
            raise ValueError(f"Student with id {id} not found")
        return student

    def select_by_faculty(self, faculty: str) -> List[StudentGrade]:
        stmt = select(StudentGrade).where(StudentGrade.faculty == faculty)
        return list(self.session.scalars(stmt).all())

    def select_unique_courses(self) -> List[str]:
        stmt = select(StudentGrade.course).distinct()
        return list(self.session.scalars(stmt).all())

    def select_average_grade_by_faculty(self, faculty: str) -> float:
        stmt = select(func.avg(StudentGrade.grade)).where(StudentGrade.faculty == faculty)
        result = self.session.scalar(stmt)
        return float(result) if result is not None else 0.0

    def select_by_course_with_low_grade(self, course: str) -> List[StudentGrade]:
        stmt = select(StudentGrade).where(
            StudentGrade.course == course,
            StudentGrade.grade < 30
        )
        return list(self.session.scalars(stmt).all())

    def insert_from_csv(self, csv_path: Path) -> None:
        student_grades = []
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                student_grade = StudentGrade(
                    last_name=row["Фамилия"],
                    first_name=row["Имя"],
                    faculty=row["Факультет"],
                    course=row["Курс"],
                    grade=int(row["Оценка"]),
                )
                student_grades.append(student_grade)
        self.insert(student_grades)

    def update_by_id(
        self,
        id: int,
        last_name: str | None = None,
        first_name: str | None = None,
        faculty: str | None = None,
        course: str | None = None,
        grade: int | None = None,
    ) -> StudentGrade:
        student = self.session.get(StudentGrade, id)
        if student is None:
            raise ValueError(f"Student with id {id} not found")
        
        if last_name is not None:
            student.last_name = last_name
        if first_name is not None:
            student.first_name = first_name
        if faculty is not None:
            student.faculty = faculty
        if course is not None:
            student.course = course
        if grade is not None:
            student.grade = grade
        
        self.session.commit()
        return student

    def delete_by_id(self, id: int) -> None:
        stmt = delete(StudentGrade).where(StudentGrade.id == id)
        result = self.session.execute(stmt)
        self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Student with id {id} not found")
