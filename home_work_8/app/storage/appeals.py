import json
from pathlib import Path
from typing import Any


class AppealsStorage:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_path.parent.mkdir(exist_ok=True)

    def _read_all(self) -> list[dict[str, Any]]:
        if not self.file_path.exists():
            return []
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, appeals: list[dict[str, Any]]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(appeals, f, ensure_ascii=False, indent=2)

    def add_appeal(self, appeal_data: dict[str, Any]) -> None:
        appeals = self._read_all()
        appeals.append(appeal_data)
        self._save(appeals)

