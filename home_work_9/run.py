from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base
from repository import StudentRepository


def main():
    db_path = Path(__file__).parent / "students.db"
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repo = StudentRepository(session)
        csv_path = Path(__file__).parent / "students.csv"
        repo.insert_from_csv(csv_path)
        
        students = repo.select_by_faculty("АВТФ")
        print(f"Found {len(students)} students from АВТФ faculty")
        
        courses = repo.select_unique_courses()
        print(f"Unique courses: {courses}")
        
        avg_grade = repo.select_average_grade_by_faculty("АВТФ")
        print(f"Average grade for АВТФ faculty: {avg_grade:.2f}")
        
        low_grade_students = repo.select_by_course_with_low_grade("Мат. Анализ")
        print(f"Students with grade < 30 in Мат. Анализ: {len(low_grade_students)}")


if __name__ == "__main__":
    main()
