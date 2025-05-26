from modules.ui.tui.menus import getInfo, printMenu, clear, yn, multiMenu
from modules.ui.tui.terminal import printObj
from modules.ui.checkers import checkINT, checkName, checkEmail, sortListsByID, findID
from modules.obj import Student, Teacher, Course, Human
from modules.database import DB
from modules.database.lookup import allRecords
from modules.ui.tui import human


class teacher(human.human):
    def printTeacher(self, msg):
        id = getInfo(
            {f"Please enter the ID of the teacher you want to {msg}.": checkINT}
        )[0]
        # If user requested to leave, go back a menu
        if (id is None):
            return

        id = int(id)
        # Convert to object for DB
        p = Teacher(Human(ID=id))
        # Get data out of DB
        table = allRecords(self.db.con.cursor(), p)
        # Get data for specific ID
        table = findID(table, id)

        p.storeLookup(Human(
            table[1],  # First name
            table[2],  # Middle Name
            table[3],  # Last Name
            table[4],  # Chosen Name
            table[5],  # Email
            table[0]  # ID
        ))

        clear()
        if (p.ID is None):
            print("There is no record for this teacher ID")
        # Prints current info for ID
        printMenu(p.printInfo())

        return p

    def viewTeachers(self):
        msg = {
            "1": "Teacher ID lookup",
            "2": "View all Teachers",
            "q": "Go Back"
        }
        while True:
            out = multiMenu(msg)

            match out:
                case "1":
                    self.printTeacher("view")
                    # Wait for user to return to menu
                    input("Press enter to return.")
                case "2":
                    self.viewAllTeachers()
                    input("Press enter to return.")
                # Exit case
                case "q": return

    def delTeacher(self):
        # Get ID and print for confirmation
        # then save object it to p
        p = self.printTeacher("delete")

        choice = yn()
        # If correct, get DB to drop
        if (choice == "y"):
            self.db.delFromDB(p)
        # Any other case, just go to last menu
        return

    def teacherMenu(self) -> None:
        msg = {
            "a": "Add Teacher",
            "r": "Remove Teacher",
            "e": "Edit Teacher",
            "v": "View Teachers",
            "q": "Go Back"
        }
        # Process kb interupt
        try:
            while True:
                out = multiMenu(msg)

                match out:
                    case "a":
                        p = self.addHuman()
                        if (p is not None):
                            self.db.saveToDB(Teacher(p))
                    case "r": self.delTeacher()
                    case "e":
                        # Call edit human with the p out from printTeacher
                        # this allows the user to confirm inputted ID
                        self.editHuman(self.printTeacher("edit"))
                    case "v": self.viewTeachers()
                    # Exit case
                    case "q": raise KeyboardInterrupt
        except KeyboardInterrupt:
            return

    def viewAllTeachers(self):
        # Sort records by ID number accending
        IDsort = sortListsByID(allRecords(
            self.db.con.cursor(),
            Teacher(Human())
        ))
        msg = [
            "ID",
            "First Name",
            "Middle Name",
            "Last Name",
            "Chosen Name",
            "Email"
        ]
        printObj(IDsort, msg)
