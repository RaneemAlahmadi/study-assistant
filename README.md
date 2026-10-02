📚 Study Assistant

A simple Python application for managing subjects, tasks, exams, deadlines, and study progress.

✨ Features

📚 Add subjects

📝 Add tasks

🧪 Add exams

📅 Set deadlines

⏳ Calculate remaining days

✅ Mark tasks and exams as completed

📊 Calculate progress percentage

🗑️ Delete tasks and exams

🗑️ Delete subjects

💾 Store all data in JSON

🧪 Unit tests

🖥️ Ready for a future Tkinter GUI

🛠️ Technologies

Python 3

JSON

Dataclasses

unittest

Tkinter (future version)

No external Python packages are required.

📁 Project Structure
study-assistant/
│
├── main.py
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── data/
│   └── study_data.json
│
├── study_assistant/
│   ├── __init__.py
│   ├── models.py
│   ├── storage.py
│   ├── service.py
│   └── cli.py
│
└── tests/
    └── test_service.py

🚀 How to Run

Make sure Python 3 is installed.

Open a terminal inside the project folder and run:

py main.py


The application will start in the terminal.

🧪 Run Tests

To run the automated tests:

py -m unittest discover -s tests -v


The tests check important features such as:

Adding subjects

Adding tasks

Adding exams

Completing items

Calculating progress

Deleting items

Saving and loading JSON data

💾 Data Storage

The application stores all study data locally in:

data/study_data.json


The data is automatically loaded when the application starts and saved whenever changes are made.

📊 Progress Calculation

Progress is calculated using:

completed items / total items × 100


For example:

5 completed / 10 total = 50%

📅 Remaining Days

The application automatically calculates the number of days remaining until each task or exam deadline.

Examples:

10 days remaining


If the deadline is today:

Due today


If the deadline has passed:

3 days overdue

🔮 Future Improvements

Possible future versions may include:

🖥️ Tkinter graphical interface

📅 Calendar view

🔎 Search and filtering

⭐ Priority levels

🔔 Notifications

🌙 Dark mode

📈 Statistics and charts

⏱️ Study sessions

📤 Export/import data

📋 More advanced deadline management

📄 License

This project is licensed under the MIT License.