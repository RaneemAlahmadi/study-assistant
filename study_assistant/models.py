from dataclasses import dataclass, field
from datetime import date
from typing import List
import uuid


@dataclass
class StudyItem:
    title: str
    due_date: str
    item_type: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    completed: bool = False

    def days_remaining(self) -> int:
        due = date.fromisoformat(self.due_date)
        return (due - date.today()).days

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "item_type": self.item_type,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            title=data["title"],
            due_date=data["due_date"],
            item_type=data["item_type"],
            completed=data.get("completed", False),
        )


@dataclass
class Subject:
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    items: List[StudyItem] = field(default_factory=list)

    def progress(self) -> float:
        if not self.items:
            return 0.0

        completed = sum(item.completed for item in self.items)
        return (completed / len(self.items)) * 100

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.to_dict() for item in self.items],
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            items=[
                StudyItem.from_dict(item)
                for item in data.get("items", [])
            ],
        )
