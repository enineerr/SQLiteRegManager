from sys import argv
from modules.ui.tui import TUI as ui


class Program:
    def __init__(self):
        self.ui = None
        self.dbPath = None
        self.main()

    def checkArgs(self, arg: str, value: str) -> int:
        match arg:
            case "dbpath" | "d": self.dbPath = value

            # Exit condition flags
            case "h" | "help":
                from modules.ui.helpmenu import helpMenu
                helpMenu()
                return 1
            case _:
                print(f"Bad CLI Flag: {arg}")
                return 2
        return 0

    def checkModules(self) -> bool:
        try:
            import sqlite3
        except ImportError:
            # Notify the user in the case its not installed
            print("Database software was not found, exiting...")
            print("Please install sqlite3 (pip install -U sqlite3)")
            return False

        return True

    def main(self) -> None:
        # Send exit code if CMDflags aren't valid
        check = 0
        # Handle cmdflags
        if len(argv) > 0:
            while (len(argv) > 0) and (check == 0):
                # Prepare for valued switch by saving next argv to var if possible
                # in order to pass to checkArgs()
                if len(argv) > 1:
                    nextArg = argv[1]
                else:
                    nextArg = ""

                # If multi char cmdflags
                if argv[0][:2] == "--":
                    check = self.checkArgs(argv[0][2:], nextArg)
                # If shorthand cmdflags
                elif argv[0][:1] == "-":
                    for i in argv[0][1:]:
                        check = self.checkArgs(i, nextArg)

                argv.pop(0)

        # Exit if cmdflags are bad
        if check != 0:
            exit(check)

        # Make sure needed modules are accessible
        # if fails, exit with error
        if self.checkModules() is False:
            exit(1)  # Exit 1 as program failed to run

        # Init UI (and DB)
        self.ui = ui(self.dbPath)


Program()
