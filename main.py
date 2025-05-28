
#!/bin/python
from sys import argv
# from modules.database import DB
# from pathlib import Path


# I apologize for this code base
# it is not efficient
# there is duplicate code
# it links backwards and forwards
# its a bit more hard coded than I like
# I just ran out of patience for my hands
# enjoy the awful table generater at modules.ui.terminal.padAllItems()
# I couldn't figure it out the next day

# I dislike the requirement to implement a sorting/filtering algorithm
# thats SQL's job
# CU wants it, so they are implemented anyway
class Program:
    def __init__(self):
        self.ui = None
        self.tui = False
        self.dbPath = None
        self.main()

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

        # Make sure needed modules are accessible, and decide on TUI or GUI
        # if either fails, exit with error
        if self.checkModules() is False:
            exit(1)  # Exit 1 as program failed to run

    def checkArgs(self, arg: str, value: str) -> int:
        match arg:
            case "tui" | "t": self.tui = True
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

        if self.tui is False:
            # Attempt loading pyqt6, if not, run only in CLI
            try:
                import PyQt6
            except ImportError:
                print("PyQt6 not found, running in TUI mode instead...")
                print("GUI can be made available with `pip install -U PyQt6`")
                self.tui = True

        # Choose UI import based on selected mode
        if self.tui is True:
            from modules.ui.tui import TUI as ui
        else:
            from modules.ui.gui import GUI as ui

        self.ui = ui(self.dbPath)

        return True


Program()
