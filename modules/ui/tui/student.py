from modules.ui.tui.menus import getInfo, printMenu, clear, yn, editHumanMenu, multiMenu
from modules.ui.checkers import checkINT, checkName, checkEmail
from modules.obj import Student, Teacher, Course, Human
from modules.database import DB
from modules.database.lookup import oneHuman
from modules.ui.tui import human


class student(human.human):
    def printStudent(self, msg):
        id = getInfo(
            {f"Please enter the ID of the student you want to {msg}.": checkINT}
        )[0]
        id = int(id)
        # Convert to object for DB
        p = Student(Human("", "", "", "", "", id))
        # Get data out of DB
        p.storeLookup(oneHuman(self.db.con.cursor(), p))

        clear()
        if (p.ID is None):
            print("There is no record for this student ID")
        # Prints current info for ID
        printMenu(p.printInfo())

        return p

    def viewStudents(self):
        msg = {
            "1": "Student ID lookup",
            "2": "View all students",
            "q": "Go Back"
        }
        while True:
            out = multiMenu(msg)

            match out:
                case "1":
                    self.printStudent("view")
                    # Wait for user to return to menu
                    input("Press enter to return.")
                case "2": self.viewAllStudents()
                # Exit case
                case "q": return

    def delStudent(self):
        # Get ID and print for confirmation
        # then save object it to p
        p = self.printStudent("delete")

        choice = yn()
        # If correct, get DB to drop
        if (choice == "y"):
            self.db.delFromDB(p)
        # Any other case, just go to last menu
        return

    def studentMenu(self) -> None:
        msg = {
            "a": "Add Student",
            "r": "Remove Student",
            "e": "Edit Student",
            "v": "View Students",
            "q": "Go Back"
        }
        while True:
            out = multiMenu(msg)

            match out:
                case "a":
                    p = self.addHuman()
                    if (p is not None):
                        self.db.saveToDB(Student(p))
                case "r": self.delStudent()
                case "e":
                    # Call edit human with the p out from printStudent
                    # this allows the user to confirm inputted ID
                    self.editHuman(self.printStudent("edit"))
                case "v": self.viewStudents()
                # Exit case
                case "q": return

    def viewAllStudents(self):
        