import tempfile
import unittest
from pathlib import Path

from study_assistant.service import StudyService
from study_assistant.storage import JSONStorage


class TestStudyService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        file_path = Path(self.temp_dir.name) / "test_data.json"

        self.storage = JSONStorage(str(file_path))
        self.service = StudyService(self.storage)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_subject(self):
        subject = self.service.add_subject("Mathematics")

        self.assertEqual(subject.name, "Mathematics")
        self.assertEqual(len(self.service.subjects), 1)

    def test_duplicate_subject(self):
        self.service.add_subject("Mathematics")

        with self.assertRaises(ValueError):
            self.service.add_subject("Mathematics")

    def test_add_task(self):
        subject = self.service.add_subject("Physics")

        item = self.service.add_item(
            subject.id,
            "Homework 1",
            "2026-12-01",
            "task",
        )

        self.assertEqual(item.title, "Homework 1")
        self.assertEqual(item.item_type, "task")

    def test_add_exam(self):
        subject = self.service.add_subject("Chemistry")

        item = self.service.add_item(
            subject.id,
            "Final Exam",
            "2026-12-20",
            "exam",
        )

        self.assertEqual(item.item_type, "exam")

    def test_complete_item(self):
        subject = self.service.add_subject("Programming")

        item = self.service.add_item(
            subject.id,
            "Project",
            "2026-12-10",
            "task",
        )

        self.assertFalse(item.completed)

        result = self.service.complete_item(
            subject.id,
            item.id,
        )

        self.assertTrue(result)
        self.assertTrue(item.completed)

    def test_progress(self):
        subject = self.service.add_subject("Math")

        first = self.service.add_item(
            subject.id,
            "Homework",
            "2026-12-01",
            "task",
        )

        self.service.add_item(
            subject.id,
            "Exam",
            "2026-12-20",
            "exam",
        )

        self.assertEqual(subject.progress(), 0)

        self.service.complete_item(
            subject.id,
            first.id,
        )

        self.assertEqual(subject.progress(), 50)

    def test_delete_item(self):
        subject = self.service.add_subject("English")

        item = self.service.add_item(
            subject.id,
            "Essay",
            "2026-12-05",
            "task",
        )

        result = self.service.delete_item(
            subject.id,
            item.id,
        )

        self.assertTrue(result)
        self.assertEqual(len(subject.items), 0)

    def test_json_persistence(self):
        subject = self.service.add_subject("Computer Science")

        self.service.add_item(
            subject.id,
            "Python Project",
            "2026-12-15",
            "task",
        )

        new_service = StudyService(self.storage)

        self.assertEqual(len(new_service.subjects), 1)
        self.assertEqual(
            new_service.subjects[0].name,
            "Computer Science",
        )


if __name__ == "__main__":
    unittest.main()
