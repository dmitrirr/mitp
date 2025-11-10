from typing import Annotated

from fastapi import APIRouter, Depends

from ..dependencies import get_appeals_service
from ..models.appeals import AppealRequest
from ..service.appeals import AppealsService

router = APIRouter()


@router.post("/appeals/", tags=["appeals"])
async def create_appeal(
    appeal: AppealRequest,
    service: Annotated[AppealsService, Depends(get_appeals_service)],
):
    appeal_data = service.create_appeal(appeal)
    return appeal_data
