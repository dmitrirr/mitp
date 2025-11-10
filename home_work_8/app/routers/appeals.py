import json
from pathlib import Path

from fastapi import APIRouter

from ..models.appeals import AppealRequest

router = APIRouter()


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

