from modules.ui.tui.menus import multiMenu
from modules.ui.checkers import checkINT, checkName, checkEmail
from modules.obj import Student, Teacher, Course, Human
from pathlib import Path
from modules.database import DB
from modules.ui.tui import student, teacher, course


class TUI(student.student, teacher.teacher, course.course):
    def __init__(self, dbpath: Path | None = None):
        # Init DB
        if dbpath is None:
            self.db = DB()
        else:
            self.db = DB(dbpath)

        # encrpytion setup

        self.mainMenu()
        self.db.close()

    def mainMenu(self) -> None:
        msg = {
            "s": "Manage Students",
            "t": "Manage Teachers",
            "c": "Manage Courses",
            "q": "Exit",
            "Press CTRL+C to go back a menu at any point.": ""
        }
        # Process kb interupt
        try:
            # Main loop for whole TUI
            while True:
                out = multiMenu(msg)
                match out:
                    case "s": self.studentMenu()
                    case "t": self.teacherMenu()
                    case "c": self.courseMenu()
                    # Exit case
                    case "q": raise KeyboardInterrupt
        except KeyboardInterrupt:
            return
