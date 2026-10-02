from datetime import date

from .models import Subject, StudyItem
from .storage import JSONStorage


class StudyService:
    def __init__(self, storage: JSONStorage):
        self.storage = storage
        self.subjects = self.storage.load()

    # -------------------------
    # Subject operations
    # -------------------------

    def add_subject(self, name: str) -> Subject:
        name = name.strip()

        if not name:
            raise ValueError("Subject name cannot be empty.")

        if any(
            subject.name.lower() == name.lower()
            for subject in self.subjects
        ):
            raise ValueError("This subject already exists.")

        subject = Subject(name=name)
        self.subjects.append(subject)
        self.save()

        return subject

    def get_subject(self, subject_id: str) -> Subject | None:
        for subject in self.subjects:
            if subject.id == subject_id:
                return subject

        return None

    def get_subject_by_name(self, name: str) -> Subject | None:
        for subject in self.subjects:
            if subject.name.lower() == name.lower():
                return subject

        return None

    def delete_subject(self, subject_id: str) -> bool:
        subject = self.get_subject(subject_id)

        if not subject:
            return False

        self.subjects.remove(subject)
        self.save()

        return True

    # -------------------------
    # Item operations
    # -------------------------

    def add_item(
        self,
        subject_id: str,
        title: str,
        due_date: str,
        item_type: str,
    ) -> StudyItem:

        subject = self.get_subject(subject_id)

        if not subject:
            raise ValueError("Subject not found.")

        title = title.strip()

        if not title:
            raise ValueError("Title cannot be empty.")

        if item_type not in ("task", "exam"):
            raise ValueError("Item type must be 'task' or 'exam'.")

        try:
            date.fromisoformat(due_date)
        except ValueError:
            raise ValueError(
                "Invalid date. Use YYYY-MM-DD."
            )

        item = StudyItem(
            title=title,
            due_date=due_date,
            item_type=item_type,
        )

        subject.items.append(item)
        self.save()

        return item

    def get_item(
        self,
        subject_id: str,
        item_id: str,
    ) -> StudyItem | None:

        subject = self.get_subject(subject_id)

        if not subject:
            return None

        for item in subject.items:
            if item.id == item_id:
                return item

        return None

    def complete_item(
        self,
        subject_id: str,
        item_id: str,
    ) -> bool:

        item = self.get_item(subject_id, item_id)

        if not item:
            return False

        item.completed = True
        self.save()

        return True

    def toggle_item(
        self,
        subject_id: str,
        item_id: str,
    ) -> bool:

        item = self.get_item(subject_id, item_id)

        if not item:
            return False

        item.completed = not item.completed
        self.save()

        return True

    def delete_item(
        self,
        subject_id: str,
        item_id: str,
    ) -> bool:

        subject = self.get_subject(subject_id)

        if not subject:
            return False

        item = self.get_item(subject_id, item_id)

        if not item:
            return False

        subject.items.remove(item)
        self.save()

        return True

    # -------------------------
    # Statistics
    # -------------------------

    def overall_progress(self) -> float:
        items = [
            item
            for subject in self.subjects
            for item in subject.items
        ]

        if not items:
            return 0.0

        completed = sum(item.completed for item in items)

        return (completed / len(items)) * 100

    def total_items(self) -> int:
        return sum(
            len(subject.items)
            for subject in self.subjects
        )

    def completed_items(self) -> int:
        return sum(
            sum(item.completed for item in subject.items)
            for subject in self.subjects
        )

    def pending_items(self) -> int:
        return (
            self.total_items()
            - self.completed_items()
        )

    def save(self) -> None:
        self.storage.save(self.subjects)
