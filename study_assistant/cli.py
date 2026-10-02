from .service import StudyService


class StudyCLI:
    def __init__(self, service: StudyService):
        self.service = service

    def run(self):
        while True:
            self.show_header()
            self.show_dashboard()
            self.show_menu()

            choice = input("\nChoose an option: ").strip()

            try:
                if choice == "1":
                    self.list_subjects()

                elif choice == "2":
                    self.add_subject()

                elif choice == "3":
                    self.view_subject()

                elif choice == "4":
                    self.add_item()

                elif choice == "5":
                    self.complete_item()

                elif choice == "6":
                    self.delete_item()

                elif choice == "7":
                    self.delete_subject()

                elif choice == "8":
                    self.show_dashboard()
                    input("\nPress Enter to continue...")

                elif choice == "0":
                    print("\nGoodbye! Keep studying! 📚")
                    break

                else:
                    print("\nInvalid option.")

            except ValueError as error:
                print(f"\nError: {error}")

            input("\nPress Enter to continue...")

    def show_header(self):
        print("\n" + "=" * 60)
        print("                 STUDY ASSISTANT")
        print("=" * 60)

    def show_menu(self):
        print("""
1. List subjects
2. Add subject
3. View subject
4. Add task/exam
5. Complete task/exam
6. Delete task/exam
7. Delete subject
8. Show dashboard
0. Exit
""")

    def show_dashboard(self):
        progress = self.service.overall_progress()

        print("\nDashboard")
        print("-" * 60)
        print(f"Subjects : {len(self.service.subjects)}")
        print(f"Total    : {self.service.total_items()}")
        print(f"Completed: {self.service.completed_items()}")
        print(f"Pending  : {self.service.pending_items()}")
        print(f"Progress : {progress:.1f}%")
        print("-" * 60)

    def list_subjects(self):
        if not self.service.subjects:
            print("\nNo subjects found.")
            return

        print("\nSubjects")
        print("-" * 60)

        for index, subject in enumerate(
            self.service.subjects,
            start=1
        ):
            print(
                f"{index}. {subject.name} "
                f"- {subject.progress():.1f}% "
                f"({len(subject.items)} items)"
            )

            print(f"   ID: {subject.id}")

    def add_subject(self):
        name = input("\nSubject name: ")

        subject = self.service.add_subject(name)

        print(
            f"\nSubject '{subject.name}' "
            "added successfully."
        )

    def select_subject(self):
        if not self.service.subjects:
            print("\nNo subjects available.")
            return None

        self.list_subjects()

        subject_id = input(
            "\nEnter subject ID: "
        ).strip()

        subject = self.service.get_subject(subject_id)

        if not subject:
            print("\nSubject not found.")
            return None

        return subject

    def view_subject(self):
        subject = self.select_subject()

        if not subject:
            return

        print("\n" + "=" * 60)
        print(f"Subject: {subject.name}")
        print(f"Progress: {subject.progress():.1f}%")
        print("=" * 60)

        if not subject.items:
            print("No tasks or exams.")
            return

        for index, item in enumerate(
            subject.items,
            start=1
        ):
            status = (
                "DONE"
                if item.completed
                else "PENDING"
            )

            days = item.days_remaining()

            if days > 0:
                time_text = (
                    f"{days} day(s) remaining"
                )
            elif days == 0:
                time_text = "Due today"
            else:
                time_text = (
                    f"{abs(days)} day(s) overdue"
                )

            print(
                f"\n{index}. "
                f"[{item.item_type.upper()}] "
                f"{item.title}"
            )

            print(f"   Date   : {item.due_date}")
            print(f"   Status : {status}")
            print(f"   Time   : {time_text}")
            print(f"   ID     : {item.id}")

    def add_item(self):
        subject = self.select_subject()

        if not subject:
            return

        title = input(
            "\nTask/Exam title: "
        ).strip()

        print("\n1. Task")
        print("2. Exam")

        item_choice = input("Type: ").strip()

        if item_choice == "1":
            item_type = "task"

        elif item_choice == "2":
            item_type = "exam"

        else:
            print("\nInvalid type.")
            return

        due_date = input(
            "Due date (YYYY-MM-DD): "
        ).strip()

        item = self.service.add_item(
            subject.id,
            title,
            due_date,
            item_type,
        )

        print(
            f"\n{item.item_type.capitalize()} "
            f"'{item.title}' added successfully."
        )

    def complete_item(self):
        subject = self.select_subject()

        if not subject:
            return

        self.view_subject()

        item_id = input(
            "\nEnter item ID to mark as complete: "
        ).strip()

        if self.service.complete_item(
            subject.id,
            item_id
        ):
            print("\nItem marked as completed.")

        else:
            print("\nItem not found.")

    def delete_item(self):
        subject = self.select_subject()

        if not subject:
            return

        self.view_subject()

        item_id = input(
            "\nEnter item ID to delete: "
        ).strip()

        if self.service.delete_item(
            subject.id,
            item_id
        ):
            print("\nItem deleted.")

        else:
            print("\nItem not found.")

    def delete_subject(self):
        subject = self.select_subject()

        if not subject:
            return

        confirmation = input(
            f"\nDelete '{subject.name}' "
            "and all its items? (y/n): "
        ).strip().lower()

        if confirmation != "y":
            print("\nDeletion cancelled.")
            return

        if self.service.delete_subject(
            subject.id
        ):
            print("\nSubject deleted.")

        else:
            print("\nSubject not found.")
