from pathlib import Path

from .service.appeals import AppealsService
from .storage.appeals import AppealsStorage

_appeals_storage: AppealsStorage | None = None
_appeals_service: AppealsService | None = None


def get_appeals_storage() -> AppealsStorage:
    global _appeals_storage
    if _appeals_storage is None:
        file_path = Path("data") / "appeals.json"
        _appeals_storage = AppealsStorage(file_path)
    return _appeals_storage


def get_appeals_service() -> AppealsService:
    global _appeals_service
    if _appeals_service is None:
        _appeals_service = AppealsService(get_appeals_storage())
    return _appeals_service

