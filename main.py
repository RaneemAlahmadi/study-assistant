from study_assistant.gui import StudyGUI
from study_assistant.service import StudyService
from study_assistant.storage import JSONStorage


def main():
    storage = JSONStorage("data/study_data.json")
    service = StudyService(storage)

    app = StudyGUI(service)
    app.run()


if __name__ == "__main__":
    main()
