import csv
from pathlib import Path
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import StudentGrade


class StudentRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert(self, items: List[StudentGrade]) -> None:
        self.session.add_all(items)
        self.session.commit()

    def select(self) -> List[StudentGrade]:
        stmt = select(StudentGrade)
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
