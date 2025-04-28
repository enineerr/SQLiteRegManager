class GUI:
    def __init__(self) -> None:
        pass

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


class TUI:
    def __init__(self):
        pass

    def maxLineLength(calcLines: list[str]) -> int:
        maxLength = 0
        for i in calcLines:
            if len(i) > maxLength:
                maxLength = len(i)
        return maxLength

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
    # Teachers
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


class helpMenu:
    def __init__(self):
        msg = {
            "-h --help": "Print this message",
            "-t --tui": "Enable TUI mode",
            "-d --dbpath <path>": "Set path to the data dir relative to CWD"
        }
        # Get max length of cmdflag side of help menu
        maxLengthKey = TUI.maxLineLength(msg.keys()) + 2

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
