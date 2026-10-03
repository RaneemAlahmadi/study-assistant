# Study Assistant

A simple Python application for managing subjects, tasks, exams, deadlines, and study progress.

## Features

- **Subject Management**
  - Create subjects
  - View subjects
  - Delete subjects

- **Task Management**
  - Add tasks
  - Set task deadlines
  - Mark tasks as completed
  - Delete tasks

- **Exam Management**
  - Add exams
  - Set exam dates
  - Mark exams as completed
  - Delete exams

- **Deadline Tracking**
  - Calculate the number of days remaining
  - Show when an item is due today
  - Show overdue items

- **Progress Tracking**
  - Calculate the overall completion percentage

- **JSON Data Storage**
  - Save all study data locally
  - Load saved data automatically

- **Automated Testing**
  - Test the application's core functionality using `unittest`

- **Graphical Interface**
  - Use a Tkinter interface to interact with the application

## Technologies

- **Python 3**
- **Tkinter**
- **JSON**
- **Dataclasses**
- **unittest**

No external Python packages are required.

## Project Structure

```text
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
│   ├── cli.py
│   └── gui.py
│
└── tests/
    └── test_service.py
```

## Getting Started

### Requirements

- Python 3
- Windows, macOS, or Linux

No additional packages are required.

### Running the Application

Open a terminal inside the project folder and run:

```bash
py main.py
```

The Tkinter graphical interface will open automatically.

## Running Tests

Run the automated tests with:

```bash
py -m unittest discover -s tests -v
```

The test suite covers functionality including:

- Adding subjects
- Adding tasks
- Adding exams
- Completing items
- Calculating progress
- Deleting items
- Saving data
- Loading data

## Progress Calculation

The application calculates progress using:

```text
Completed Items / Total Items × 100
```

For example:

```text
Completed Items: 5
Total Items: 10

Progress: 50%
```

## Deadline Tracking

The application calculates the remaining time for every task and exam.

For example:

```text
10 days remaining
```

If the deadline is today:

```text
Due today
```

If the deadline has passed:

```text
3 days overdue
```

## Data Storage

All application data is stored locally in:

```text
data/study_data.json
```

The application automatically loads existing data when it starts and saves changes when data is modified.

## Command-Line Interface

The project also contains a command-line interface in:

```text
study_assistant/cli.py
```

The CLI provides an alternative way to interact with the application without using the graphical interface.

## Graphical Interface

The graphical interface is implemented using Python's built-in Tkinter library.

The GUI provides:

- Subject management
- Task management
- Exam management
- Completion controls
- Progress tracking
- Deadline information
- Data persistence

## Future Improvements

- Calendar view
- Search and filtering
- Priority levels
- Notifications
- Dark mode
- Statistics and charts
- Study sessions
- Data export and import
- Advanced deadline management

## License

This project is licensed under the MIT License.
