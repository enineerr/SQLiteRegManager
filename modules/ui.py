from pathlib import Path
from modules.database import DB
from modules.obj import Student, Teacher, Course, Human


class UI:
    def __init__(self, dbpath: Path | None = None):
        if dbpath is None:
            self.db = DB()
        else:
            self.db = DB(dbpath)

    def closeDB(self) -> None:
        self.db.close()

    @staticmethod
    def checkName(inp: str) -> bool:
        for i in inp:
            if i == " ":
                return False
            elif i == "-":
                pass
            elif i.isalpha() is not True:
                return False

        return True

    @staticmethod
    def checkEmail(inp: str) -> bool:
        hasAt = False
        hasDot = False
        for i in inp:
            if i == "@":
                hasAt = True
            elif i == ".":
                hasDot = True

        return (hasAt and hasDot)

    @staticmethod
    def checkYN(inp: str) -> bool:
        match inp.lower()[:1]:
            case "y" | "n": return True
            case _: return False

    @staticmethod
    def checkINT(inp: str) -> bool:
        if inp.isnumeric():
            return True
        return False


class GUI(UI):
    # def __init__(self) -> None:
    #     pass

    #
    # Students
    #
    def PasswordUI(self) -> None:
        pass

    def AddStudent(self) -> None:
        pass

    def RemoveStudent(self) -> None:
        pass

    def EditStudent(self) -> None:
        pass

    #
    # TEACHERS
    #
    def AddTeacher(self) -> None:
        pass

    def RemoveTeacher(self) -> None:
        pass

    def EditTeacher(self) -> None:
        pass

    #
    # Courses
    #
    def AddCourse(self) -> None:
        pass

    def RemoveCourse(self) -> None:
        pass

    def EditCourse(self) -> None:
        pass


class TUI(UI):
    # def __init__(self, dbpath: Path | None = None):
    #     self.dbinit(dbpath)

    @staticmethod
    def maxLineLength(calcLines: list[str]) -> int:
        maxLength = 0
        for i in calcLines:
            if len(i) > maxLength:
                maxLength = len(i)
        return maxLength

    @staticmethod
    def printMenu(msg: dict[str, str]) -> None:
        for k, v in msg.items():
            # Add a basic separator
            k += ":"
            print(k, v)

    # @staticmethod
    # def printPaddedMenu(msg: dict[str, str]) -> None:
    #     maxLengthKey = TUI.maxLineLength(list(msg.keys())) + 2

    #     # Create a list of combined keys and values for calculation
    #     dictCombined = [k + v for k, v in msg.items()]
    #     # Get max length
    #     maxLengthLine = TUI.maxLineLength(dictCombined) + 4

    #     print("-" * maxLengthLine)
    #     for k, v in msg.items():
    #         # Add a basic separator
    #         k += ": "
    #         print(k.ljust(maxLengthKey) + v)

    #         print("-" * maxLengthLine)

    @staticmethod
    def clear() -> None:
        # I dont like this
        # the day python implements a terminal clear, the world will be whole
        print("\n"*100)

    @staticmethod
    def checkInput(func) -> bool | str:
        inp = input(">>> ")
        # If name is valid, move to next loop
        if func(inp):
            return inp
        else:
            TUI.clear()
            print("Please re-enter, invalid character entered.")
            return False

    @staticmethod
    def getInfo() -> Human | None:
        # First Name
        # clear terminal
        TUI.clear()
        # Check flag - if entered text is valid
        accepted = False
        while (accepted is False):
            print("Please enter the first name.")
            accepted = TUI.checkInput(TUI.checkName)

        # Save input to var
        firstName = accepted

        # Last Name
        # clear terminal
        TUI.clear()
        accepted = False
        while (accepted is False):
            print("Please enter the last name.")
            accepted = TUI.checkInput(TUI.checkName)

        # Save input to var
        lastName = accepted

        # Middle name
        # clear terminal
        TUI.clear()
        accepted = False
        while (accepted is False):
            print("Please enter the middle name.")
            accepted = TUI.checkInput(TUI.checkName)

        # Save input to var
        middleName = accepted

        # Chosen name
        TUI.clear()
        accepted = False
        while (accepted is False):
            print("Please enter the chosen name.")
            accepted = TUI.checkInput(TUI.checkName)

        # Save input to var
        chosenName = accepted

        # Email
        TUI.clear()
        accepted = False
        while (accepted is False):
            print("Please enter the email.")
            accepted = TUI.checkInput(TUI.checkEmail)

        # Save input to var
        email = accepted

        TUI.clear()
        p = Human(
            firstName,
            middleName,
            lastName,
            chosenName,
            email
        )
        # Print info
        TUI.printMenu(p.printInfo())
        accepted = False
        while (accepted is False):
            print("Is this correct?")
            accepted = TUI.checkInput(TUI.checkYN)

        match accepted.lower()[0]:
            case "y": return p
            case "n": return

    # @staticmethod
    def mainMenu(self) -> None:
        msg = {
            "(s)": "Manage Students",
            "(t)": "Manage Teachers",
            "(c)": "Manage Courses",
            "(r)": "Manage Registrations",
            "(q)": "Exit"
        }

        while True:
            TUI.clear()
            TUI.printMenu(msg)

            inp = input(">>> ")

            match inp.lower():
                case "s": self.studentMenu()
                case "t": self.teacherMenu()
                case "c": self.courseMenu()
                case "r": self.coureMenu()

                # Exit the app cleanly
                case "q":
                    self.db.close()
                    exit()

                # If invalid input, restart loop, skipping exit
                case _: continue

    def passwordUI(self) -> None:
        pass

    #
    # Students
    #
    def studentMenu(self) -> None:
        msg = {
            "(a)": "Add Student",
            "(r)": "Remove Student",
            "(e)": "Edit Student",
            "(v)": "View Students",
            "(q)": "Go Back"
        }

        while True:
            TUI.clear()
            TUI.printMenu(msg)

            inp = input(">>> ")

            # Process input
            match inp.lower():
                case "a": self.addStudent()
                case "r": self.removeStudent()
                case "e": self.editStudent()
                case "v": self.viewStudents()
                case "q": return
                # If invalid input, restart loop, skipping exit
                case _: continue

    def addStudent(self) -> None:
        p = TUI.getInfo()
        if p is None:
            return

        # Convert Human to Student, and save to DB
        self.db.saveToDB(Student(p))

    def removeStudent(self) -> None:
        # Get user's ID
        accepted = False
        while (accepted is False):
            print("Please enter the ID of the student you want to remove.")
            accepted = TUI.checkInput(TUI.checkINT)
        # Save for lookup
        id = int(accepted)

        # Get data of ID
        p = self.db.lookupStudentDB(id)

        # Print data about ID
        TUI.printMenu(p.printInfo())
        accepted = False
        while (accepted is False):
            print("Is this correct? (y/n)")
            accepted = TUI.checkInput(TUI.checkYN)

        match accepted.lower()[0]:
            case "n": return
            case "y":
                self.db.delFromDB(p)


    def editStudent(self) -> None:
        pass

    #
    # Teachers
    #
    def addTeacher(self) -> None:
        pass

    def removeTeacher(self) -> None:
        pass

    def editTeacher(self) -> None:
        pass

    #
    # Courses
    #
    def addCourse(self) -> None:
        pass

    def removeCourse(self) -> None:
        pass

    def editCourse(self) -> None:
        pass


class helpMenu:
    def __init__(self):
        msg = {
            "-h --help": "Print this message",
            "-t --tui": "Enable TUI mode",
            "-d --dbpath <path>": "Set path to the data dir relative to CWD"
        }
        # Get max length of cmdflag side of help menu
        maxLengthKey = TUI.maxLineLength(list(msg.keys())) + 2

        # Create a list of combined keys and values for calculation
        dictCombined = [k + v for k, v in msg.items()]
        # Get max length
        maxLengthLine = TUI.maxLineLength(dictCombined) + 4

        print("-" * maxLengthLine)
        for k, v in msg.items():
            # Add a basic separator
            k += ": "
            print(k.ljust(maxLengthKey) + v)

            print("-" * maxLengthLine)
