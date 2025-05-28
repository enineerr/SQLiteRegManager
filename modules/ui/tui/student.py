from modules.ui.tui.menus import getInfo, printMenu, clear, yn, multiMenu
from modules.ui.tui.terminal import printObj
from modules.ui.checkers import checkINT, checkName, checkEmail, sortListsByID, findID, findAllIDs
from modules.obj import Student, Teacher, Course, Human, sReg, tReg, Reg
from modules.database import DB
from modules.database.lookup import allRecords, getRegistrations
from modules.ui.tui import human


class student(human.human):
    def printStudent(self, msg) -> Student | None:
        id = getInfo(
            {f"Please enter the ID of the student you want to {msg}.": checkINT}
        )[0]
        # If user requested to leave, go back a menu
        if (id is None):
            return

        id = int(id)
        # Convert to object for DB
        p = Student(Human(ID=id))
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
            print("There is no record for this student ID")
        # Prints current info for ID
        printMenu(p.printInfo())

        return p

    def viewStudents(self) -> None:
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
                case "2":
                    self.viewAllStudents()
                    input("Press enter to return.")
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
            "c": "Course Registrations",
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
                            try:
                                self.db.saveToDB(Student(p))
                            except ValueError:
                                clear()
                                print("Email address already in use.")
                                input("Press enter to return.")
                    case "r": self.delStudent()
                    case "e":
                        # Call edit human with the p out from printStudent
                        # this allows the user to confirm inputted ID
                        self.editHuman(self.printStudent("edit"))
                    case "v": self.viewStudents()
                    case "c": self.regStudentMenu()
                    # Exit case
                    case "q": raise KeyboardInterrupt
        except KeyboardInterrupt:
            return

    def viewAllStudents(self) -> None:
        # Sort records by ID number accending
        IDsort = sortListsByID(allRecords(
            self.db.con.cursor(),
            Student(Human())
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

    def regStudentMenu(self) -> None:
        msg = {
            "1": "Register Student to Course",
            "2": "Deregister Student from Course",
            "3": "View Registrations By IDs",
            "4": "View All Registrations",
            "q": "Go Back"
        }
        while True:
            try:
                out = multiMenu(msg)

                match out:
                    case "1":
                        self.registerStudent()
                    case "2":
                        self.deregisterStudent()
                    case "3":
                        try:
                            r = self.getSReg(["view", "view"])
                            # If they returned from the menu, just start over
                            if (r is None):
                                continue
                            self.viewSRegs(r)
                            input("Press enter to return.")
                        except KeyboardInterrupt:
                            pass
                    case "4":
                        self.viewSRegs()
                        input("Press enter to return.")
                    # Exit case
                    case "q": return
            except KeyboardInterrupt:
                return

    def registerStudent(self) -> None:
        try:
            r = self.getSReg(
                [
                    "register",
                    "register to"
                ]
            )
            if (r is None):
                return
            # Save reg to db
            try:
                self.db.saveToDB(r)
            except ValueError:
                clear()
                print("Student has already been registered for this course.")
                input("Press enter to return.")
        except KeyboardInterrupt:
            return

    def deregisterStudent(self) -> None:
        try:
            r = self.getSReg(
                [
                    "deregister",
                    "deregister from"
                ]
            )
            if (r is None):
                return
            filtered = self.viewSRegs(r)
            choice = yn()
            if (choice == "n"):
                return
            self.db.delFromDB(sReg(Reg(ID=filtered[0][8])))

        except KeyboardInterrupt:
            return

    def getSReg(self, msg: list[str]) -> sReg | None:
        # Get student ID and info
        p = self.printStudent(msg[0])
        if (p is None):
            return
        # Check if correct
        choice = yn()
        if (choice == "n"):
            return
        # If p ID was invalid, exit
        if (p.ID is None):
            return

        # Get course ID and info
        c = self.printCourse(msg[1])
        if (c is None):
            return
        # Check if correct
        choice = yn()
        if (choice == "n"):
            return
        # If c ID was invalid, exit
        if (c.ID is None):
            return

        return sReg(Reg(p.ID, c.ID))

    def viewSRegs(self, obj: sReg = sReg(Reg())) -> list[list[str | int]]:
        # Get all records
        filtered = getRegistrations(self.db.con.cursor(), obj)
        # If IDs were specified, filter the list
        if (obj.cID is not None):
            filtered = findAllIDs(filtered, obj.hID, 0)
            filtered = findAllIDs(filtered, obj.cID, 4)

        printObj(
            filtered,
            [
                "SID",
                "First Name",
                "Last Name",
                "Chosen Name",
                "Course ID",
                "Course Name",
                "Level",
                "Registration Time",
                "RID"
            ]
        )
        return filtered