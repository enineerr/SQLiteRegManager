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
        # if blank, allow to continue
        if inp == "":
            return True

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
    # Fairly self explanatory
    # calculates the longest string length of a list
    @staticmethod
    def maxLineLength(calcLines: list[str]) -> int:
        maxLength = 0
        for i in calcLines:
            if len(i) > maxLength:
                maxLength = len(i)
        return maxLength

    # Take a dict, and print it line by line, separating keys and values using ": "
    @staticmethod
    def printMenu(msg: dict[str, str]) -> None:
        for k, v in msg.items():
            # Add a basic separator
            k += ":"
            print(k, v)

    @staticmethod
    def clear() -> None:
        # I dont like this
        # the day python implements a terminal clear, the world will be whole
        print("\n"*100)

    # Takes a function as an arg,
    # then takes an input from user,
    # and uses function to check if valid,
    # if valid, returns input
    # else, false
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

    # Basic yes or no check
    @staticmethod
    def yn() -> str:
        accepted = False
        while (accepted is False):
            print("Is this correct? (y/n)")
            accepted = TUI.checkInput(TUI.checkYN)

        return accepted

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
            print("Is this correct? (y/n)")
            accepted = TUI.checkInput(TUI.checkYN)

        match accepted.lower()[0]:
            case "y": return p
            case "n": return

    # Generic menu for editing a person's information
    # Edit menu:
    # 1-5 choose field to edit, returns 1-5
    # q exits the menu, returns 0 (would be ID index if used)
    @staticmethod
    def editHumanMenu() -> int:
        msg = {
            "(1)": "Edit First Name",
            "(2)": "Edit Middle Name",
            "(3)": "Edit Last Name",
            "(4)": "Edit Chosen Name",
            "(5)": "Edit Email",
            "(q)": "Go Back"
        }

        while True:
            TUI.clear()
            TUI.printMenu(msg)

            inp = input(">>> ")

            # Process input
            match inp.lower():
                case "1" | "2" | "3" | "4" | "5":
                    return int(inp)
                case "q": return 0
                # If invalid input, restart loop, skipping exit
                case _: continue

    @staticmethod
    def viewMenu() -> int:
        # TODO put another layer into this after 2 for sorting records better?
        msg = {
            "(1)": "View 1 record",
            "(2)": "View all records",
            "(q)": "Go Back"
        }

        while True:
            TUI.clear()
            TUI.printMenu(msg)

            inp = input(">>> ")

            # Process input
            match inp.lower():
                case "1" | "2":
                    return int(inp)
                case "q": return 0
                # If invalid input, restart loop, skipping exit
                case _: continue

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
            TUI.clear()
            print("Please enter the ID of the student you want to remove.")
            accepted = TUI.checkInput(TUI.checkINT)
        # Save for lookup
        id = int(accepted)

        # Create (mostly) blank instance, to be filled in later
        p = Student(Human("", "", "", "", "", id))
        # Get data of ID
        p = Student(self.db.lookupDB(p))

        TUI.clear()
        # Print data about ID
        TUI.printMenu(p.printInfo())
        accepted = TUI.yn()

        match accepted.lower()[0]:
            case "n": return
            case "y":
                self.db.delFromDB(p)

    def editStudent(self) -> None:
        # TODO refactor this and removeStudent()
        # TODO maybe make it separate functions which do not need hardcoded student/teacher
        # Get user's ID
        accepted = False
        while (accepted is False):
            TUI.clear()
            print("Please enter the ID of the student you want to edit.")
            accepted = TUI.checkInput(TUI.checkINT)
        # Save for lookup
        id = int(accepted)

        # Create (mostly) blank instance, to be filled in later
        p = Student(Human("", "", "", "", "", id))
        # Get data of ID
        p = Student(self.db.lookupDB(p))

        TUI.clear()
        # Print data about ID
        TUI.printMenu(p.printInfo())
        accepted = TUI.yn()

        # If wrong, go back a menu
        if (accepted.lower()[0] == "n"):
            return

        choice = TUI.editHumanMenu()

        if (choice == 0):
            return

        msgs = [
            f"Editing First Name: {p.firstName}",
            f"Editing Middle Name: {p.middleName}",
            f"Editing Last Name: {p.lastName}",
            f"Editing Chosen Name: {p.chosenName}",
            f"Editing Email address: {p.email}",
        ]

        accepted = False
        while (accepted is False):
            print(msgs[choice - 1])
            if (choice == 5):
                accepted = TUI.checkInput(TUI.checkEmail)
            else:
                accepted = TUI.checkInput(TUI.checkName)

        match choice:
            case 1: p.firstName = accepted
            case 2: p.middleName = accepted
            case 3: p.lastName = accepted
            case 4: p.chosenName = accepted
            case 5: p.email = accepted

        self.db.updateDB(p)

    def viewStudents(self) -> None:
        choice = TUI.viewMenu()
        if choice == 1:
            accepted = False
            while (accepted is False):
                TUI.clear()
                print("Please enter the ID of the student you want to edit.")
                accepted = TUI.checkInput(TUI.checkINT)
            # Save for lookup
            id = int(accepted)

            # Create (mostly) blank instance, to be filled in later
            p = Student(Human("", "", "", "", "", id))
            # Get data of ID
            p = Student(self.db.lookupDB(p))

            TUI.clear()
            # Print data about ID
            TUI.printMenu(p.printInfo())

            input("Press enter to return.")
        # else:
        #     pass

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
