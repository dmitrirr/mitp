from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_students_service
from ..models.students import StudentCreate, StudentResponse, StudentUpdate
from ..service.students import StudentsService

router = APIRouter()


@router.post("/students/", response_model=StudentResponse)
async def create_student(
    student: StudentCreate,
    service: Annotated[StudentsService, Depends(get_students_service)],
):
    try:
        return service.create_student(student)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/students/", response_model=List[StudentResponse])
async def get_students(
    service: Annotated[StudentsService, Depends(get_students_service)],
):
    return service.get_students()


@router.get("/students/{id}", response_model=StudentResponse)
async def get_student(
    id: int,
    service: Annotated[StudentsService, Depends(get_students_service)],
):
    try:
        return service.get_student_by_id(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/students/{id}", response_model=StudentResponse)
async def update_student(
    id: int,
    student: StudentUpdate,
    service: Annotated[StudentsService, Depends(get_students_service)],
):
    try:
        return service.update_student(id, student)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/students/{id}")
async def delete_student(
    id: int,
    service: Annotated[StudentsService, Depends(get_students_service)],
):
    try:
        service.delete_student(id)
        return {"message": "Student deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
