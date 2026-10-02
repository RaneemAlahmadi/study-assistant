import json
from pathlib import Path

from .models import Subject


class JSONStorage:
    def __init__(self, file_path: str = "data/study_data.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[Subject]:
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            return [
                Subject.from_dict(subject)
                for subject in data.get("subjects", [])
            ]

        except (json.JSONDecodeError, KeyError, TypeError):
            return []

    def save(self, subjects: list[Subject]) -> None:
        data = {
            "subjects": [
                subject.to_dict()
                for subject in subjects
            ]
        }

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )
