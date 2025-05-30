from modules.ui.tui.menus import getInfo, printMenu, clear, yn, multiMenu
from modules.ui.tui.terminal import printObj
from modules.ui.checkers import checkINT, sortListsByID, findID, findAllIDs
from modules.obj import Teacher, Human, tReg, Reg
from modules.database.lookup import allRecords, getRegistrations
from modules.ui.tui import human


class teacher(human.human):
    def teacherMenu(self) -> None:
        msg = {
            "a": "Add Teacher",
            "r": "Remove Teacher",
            "e": "Edit Teacher",
            "v": "View Teachers",
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
                                self.db.saveToDB(Teacher(p))
                            except ValueError:
                                clear()
                                print(f"Email address already in use. ({p.email})")
                                input("Press enter to return.")
                    case "r": self.delTeacher()
                    case "e":
                        # Call edit human with the p out from printTeacher
                        # this allows the user to confirm inputted ID
                        self.editHuman(self.printTeacher("edit"))
                    case "v": self.viewTeachers()
                    case "c": self.regTeacherMenu()
                    # Exit case
                    case "q": raise KeyboardInterrupt
        except KeyboardInterrupt:
            return

    def printTeacher(self, msg) -> Teacher | None:
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

        # Store new data back to p object
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

    def viewTeachers(self) -> None:
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

    def viewAllTeachers(self) -> None:
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

    def regTeacherMenu(self) -> None:
        msg = {
            "1": "Register Teacher to Course",
            "2": "Deregister Teacher from Course",
            "3": "View Registrations By IDs",
            "4": "View All Registrations",
            "q": "Go Back"
        }
        while True:
            try:
                out = multiMenu(msg)

                match out:
                    case "1":
                        self.registerTeacher()
                    case "2":
                        self.deregisterTeacher()
                    case "3":
                        try:
                            r = self.getTReg(["view", "view"])
                            # If they returned from the menu, just start over
                            if (r is None):
                                continue
                            self.viewTRegs(r)
                            input("Press enter to return.")
                        except KeyboardInterrupt:
                            pass
                    case "4":
                        self.viewTRegs()
                        input("Press enter to return.")
                    # Exit case
                    case "q": return
            except KeyboardInterrupt:
                return

    def registerTeacher(self) -> None:
        try:
            r = self.getTReg(
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
                print("Teacher has already been registered for this course.")
                input("Press enter to return.")
        except KeyboardInterrupt:
            return

    def deregisterTeacher(self) -> None:
        try:
            r = self.getTReg(
                [
                    "deregister",
                    "deregister from"
                ]
            )
            if (r is None):
                return
            filtered = self.viewTRegs(r)
            choice = yn()
            if (choice == "n"):
                return
            self.db.delFromDB(tReg(Reg(ID=filtered[0][8])))

        except KeyboardInterrupt:
            return

    def getTReg(self, msg: list[str]) -> tReg | None:
        # Get student ID and info
        p = self.printTeacher(msg[0])
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

        return tReg(Reg(p.ID, c.ID))

    def viewTRegs(self, obj: tReg = tReg(Reg())) -> list[list[str | int]]:
        # Get all records
        filtered = getRegistrations(self.db.con.cursor(), obj)
        # If IDs were specified, filter the list
        if (obj.cID is not None):
            filtered = findAllIDs(filtered, obj.hID, 0)
            filtered = findAllIDs(filtered, obj.cID, 4)

        printObj(
            filtered,
            [
                "TID",
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

    def delTeacher(self) -> None:
        # Get ID and print for confirmation
        # then save object it to p
        p = self.printTeacher("delete")

        choice = yn()
        # If correct, get DB to drop
        if (choice == "y"):
            self.db.delFromDB(p)
        # Any other case, just go to last menu
        return
