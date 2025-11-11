from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base
from repository import StudentRepository


def main():
    db_path = Path(__file__).parent / "students.db"
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repo = StudentRepository(session)
        csv_path = Path(__file__).parent / "students.csv"
        repo.insert_from_csv(csv_path)


if __name__ == "__main__":
    main()
