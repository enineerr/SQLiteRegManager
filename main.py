#!/bin/python
from sys import argv


class Program:
    def __init__(self):
        self.tui = False
        self.dbPath = None
        self.main()

    def checkArgs(self, arg: str, value: str) -> bool:
        match arg:
            case "tui" | "t": self.tui = True
            case "dbpath" | "d": self.dbPath = value

            # Exit condition flags
            case "h" | "help":
                from modules.ui import helpMenu
                helpMenu()
                return False
            case _:
                print(f"Bad CLI Flag: {arg}")
                return False
        return True

    def main(self) -> None:
        # Handle cmdflags
        check = True
        while len(argv) > 0:
            # Prepare for valued switch
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
        if not check:
            return

        # Make sure sqlite3 library is installed
        try:
            import sqlite3
        except ImportError:
            # Notify the user in the case its not installed
            print("Database software was not found, exiting...")
            print("Please install sqlite3 (pip install -U sqlite3)")
            return

        if not self.tui:
            # Attempt loading pyqt6, if not, run only in CLI
            try:
                import PyQt6
            except ImportError:
                print("PyQt6 not found, running in TUI mode instead...")
                print("GUI can be made available with `pip install -U PyQt6`")
                self.cli = True

        # Choose UI import based on selected mode
        if self.tui:
            from modules.ui import TUI as ui
        else:
            from modules.ui import GUI as ui


Program()
