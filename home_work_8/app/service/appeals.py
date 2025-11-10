from ..models.appeals import AppealRequest
from ..storage.appeals import AppealsStorage


class AppealsService:
    def __init__(self, storage: AppealsStorage):
        self.storage = storage

    def create_appeal(self, appeal: AppealRequest) -> dict:
        appeal_data = appeal.model_dump(mode="json")
        self.storage.add_appeal(appeal_data)
        return appeal_data
