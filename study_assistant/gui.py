import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from .service import StudyService


class StudyGUI:
    def __init__(self, service: StudyService):
        self.service = service

        self.root = tk.Tk()
        self.root.title("📚 Study Assistant")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)

        self.setup_style()
        self.create_widgets()
        self.refresh()

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold"),
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11),
        )

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Segoe UI", 10),
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
        )

    def create_widgets(self):
        # Main container
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)

        # Header
        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 15))

        ttk.Label(
            header,
            text="📚 Study Assistant",
            style="Title.TLabel",
        ).pack(side="left")

        self.progress_label = ttk.Label(
            header,
            text="Progress: 0%",
            style="Subtitle.TLabel",
        )
        self.progress_label.pack(side="right")

        # Progress bar
        self.progress = ttk.Progressbar(
            main,
            orient="horizontal",
            mode="determinate",
            maximum=100,
        )
        self.progress.pack(fill="x", pady=(0, 20))

        # Content
        content = ttk.Frame(main)
        content.pack(fill="both", expand=True)

        # Subjects panel
        subjects_frame = ttk.LabelFrame(
            content,
            text="Subjects",
            padding=10,
        )
        subjects_frame.pack(
            side="left",
            fill="y",
            padx=(0, 10),
        )

        self.subject_list = tk.Listbox(
            subjects_frame,
            width=25,
            font=("Segoe UI", 11),
            activestyle="none",
        )
        self.subject_list.pack(
            fill="both",
            expand=True,
        )

        self.subject_list.bind(
            "<<ListboxSelect>>",
            self.on_subject_selected,
        )

        subject_buttons = ttk.Frame(subjects_frame)
        subject_buttons.pack(fill="x", pady=(10, 0))

        ttk.Button(
            subject_buttons,
            text="+ Add",
            command=self.add_subject,
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))

        ttk.Button(
            subject_buttons,
            text="Delete",
            command=self.delete_subject,
        ).pack(side="left", fill="x", expand=True, padx=(4, 0))

        # Items panel
        items_frame = ttk.LabelFrame(
            content,
            text="Tasks & Exams",
            padding=10,
        )
        items_frame.pack(
            side="left",
            fill="both",
            expand=True,
        )

        columns = (
            "type",
            "title",
            "date",
            "status",
            "remaining",
        )

        self.tree = ttk.Treeview(
            items_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.tree.heading("type", text="Type")
        self.tree.heading("title", text="Title")
        self.tree.heading("date", text="Due Date")
        self.tree.heading("status", text="Status")
        self.tree.heading("remaining", text="Remaining")

        self.tree.column("type", width=80)
        self.tree.column("title", width=220)
        self.tree.column("date", width=110)
        self.tree.column("status", width=100)
        self.tree.column("remaining", width=120)

        scrollbar = ttk.Scrollbar(
            items_frame,
            orient="vertical",
            command=self.tree.yview,
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        # Buttons
        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=(15, 0))

        ttk.Button(
            buttons,
            text="+ Add Task / Exam",
            command=self.add_item,
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            buttons,
            text="✓ Complete",
            command=self.complete_item,
        ).pack(side="left", padx=8)

        ttk.Button(
            buttons,
            text="Delete",
            command=self.delete_item,
        ).pack(side="left", padx=8)

        ttk.Button(
            buttons,
            text="Refresh",
            command=self.refresh,
        ).pack(side="right")

    def refresh(self):
        self.refresh_subjects()
        self.refresh_progress()

        if self.service.subjects:
            if not self.subject_list.curselection():
                self.subject_list.selection_set(0)

            self.on_subject_selected()

        else:
            self.clear_items()

    def refresh_subjects(self):
        self.subject_list.delete(0, tk.END)

        for subject in self.service.subjects:
            self.subject_list.insert(
                tk.END,
                subject.name,
            )

    def refresh_progress(self):
        progress = self.service.overall_progress()

        self.progress["value"] = progress
        self.progress_label.config(
            text=f"Progress: {progress:.1f}%"
        )

    def get_selected_subject(self):
        selection = self.subject_list.curselection()

        if not selection:
            return None

        index = selection[0]

        if index >= len(self.service.subjects):
            return None

        return self.service.subjects[index]

    def on_subject_selected(self, event=None):
        subject = self.get_selected_subject()

        if not subject:
            self.clear_items()
            return

        self.show_items(subject)

    def show_items(self, subject):
        self.clear_items()

        for item in subject.items:
            status = (
                "Completed"
                if item.completed
                else "Pending"
            )

            days = item.days_remaining()

            if days > 0:
                remaining = f"{days} days"
            elif days == 0:
                remaining = "Today"
            else:
                remaining = f"{abs(days)} overdue"

            self.tree.insert(
                "",
                tk.END,
                iid=item.id,
                values=(
                    item.item_type.capitalize(),
                    item.title,
                    item.due_date,
                    status,
                    remaining,
                ),
            )

    def clear_items(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def add_subject(self):
        name = simpledialog.askstring(
            "Add Subject",
            "Subject name:",
            parent=self.root,
        )

        if not name:
            return

        try:
            self.service.add_subject(name)
            self.refresh()

            messagebox.showinfo(
                "Success",
                "Subject added successfully.",
                parent=self.root,
            )

        except ValueError as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.root,
            )

    def delete_subject(self):
        subject = self.get_selected_subject()

        if not subject:
            messagebox.showwarning(
                "No Subject",
                "Please select a subject first.",
                parent=self.root,
            )
            return

        confirm = messagebox.askyesno(
            "Delete Subject",
            f"Delete '{subject.name}' and all its items?",
            parent=self.root,
        )

        if not confirm:
            return

        self.service.delete_subject(subject.id)
        self.refresh()

    def add_item(self):
        subject = self.get_selected_subject()

        if not subject:
            messagebox.showwarning(
                "No Subject",
                "Please select a subject first.",
                parent=self.root,
            )
            return

        title = simpledialog.askstring(
            "Add Task / Exam",
            "Title:",
            parent=self.root,
        )

        if not title:
            return

        item_type = simpledialog.askstring(
            "Item Type",
            "Type: task or exam",
            parent=self.root,
        )

        if not item_type:
            return

        item_type = item_type.lower().strip()

        if item_type not in ("task", "exam"):
            messagebox.showerror(
                "Error",
                "Type must be 'task' or 'exam'.",
                parent=self.root,
            )
            return

        due_date = simpledialog.askstring(
            "Due Date",
            "Due date (YYYY-MM-DD):",
            parent=self.root,
        )

        if not due_date:
            return

        try:
            self.service.add_item(
                subject.id,
                title,
                due_date,
                item_type,
            )

            self.refresh()

        except ValueError as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.root,
            )

    def get_selected_item(self):
        selection = self.tree.selection()

        if not selection:
            return None

        subject = self.get_selected_subject()

        if not subject:
            return None

        item_id = selection[0]

        return self.service.get_item(
            subject.id,
            item_id,
        )

    def complete_item(self):
        subject = self.get_selected_subject()
        item = self.get_selected_item()

        if not subject or not item:
            messagebox.showwarning(
                "No Item",
                "Please select a task or exam first.",
                parent=self.root,
            )
            return

        if item.completed:
            messagebox.showinfo(
                "Already Completed",
                "This item is already completed.",
                parent=self.root,
            )
            return

        self.service.complete_item(
            subject.id,
            item.id,
        )

        self.refresh()

    def delete_item(self):
        subject = self.get_selected_subject()
        item = self.get_selected_item()

        if not subject or not item:
            messagebox.showwarning(
                "No Item",
                "Please select a task or exam first.",
                parent=self.root,
            )
            return

        confirm = messagebox.askyesno(
            "Delete Item",
            f"Delete '{item.title}'?",
            parent=self.root,
        )

        if not confirm:
            return

        self.service.delete_item(
            subject.id,
            item.id,
        )

        self.refresh()

    def run(self):
        self.root.mainloop()
