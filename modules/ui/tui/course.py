from modules.ui.tui.menus import getInfo, printMenu, clear, yn, multiMenu
from modules.ui.tui.terminal import printObj
from modules.ui.checkers import checkINT, checkName, checkEmail, sortListsByID, findID
from modules.obj import Student, Teacher, Course, Human
from modules.database import DB
from modules.database.lookup import allRecords
from modules.ui.tui import human

class course:
    def addCourse(self) -> Course | None:
        info = getInfo({
            "Please enter the name of the course": checkName,
            "Please enter the level of the course": checkINT
        })
        # Return if exited by user using kb interupt
        if (info[0] is None):
            return

        c = Course(
            info[0],  # Course Name
            int(info[1])  # Course Level
        )

        clear()
        printMenu(c.printInfo())
        choice = yn()
        # If correct, return the object
        if (choice == "y"):
            return c
        # Any other case, just go to last menu
        return

    def editCourse(self, c: Course) -> None:
        if (c.ID is None):
            input("Please press enter to continue.")
            return

        # Confirm correct course, otherwise go back a menu
        choice = yn()
        if (choice == "n"):
            return

        msg = {
            "1": "Edit Course Name",
            "2": "Edit Course Level"
        }

        choice2 = multiMenu(msg)  # which field to edit
        match choice2:
            case "1":
                c.courseName = getInfo(
                    {f"Editing Course Name: {c.courseName}": checkName}
                )[0]
            case "2":
                c.level = int(getInfo(
                    {f"Editing middle Name: {c.level}": checkINT}
                )[0])
            case "q": return

        clear()
        # Confirm new info
        printMenu(c.printInfo())
        choice = yn()
        if (choice == "n"):
            return

        # Update the db with the new information
        self.db.updateDB(c)

    def printCourse(self, msg):
        id = getInfo(
            {f"Please enter the ID of the course you want to {msg}.": checkINT}
        )[0]
        # If user requested to leave, go back a menu
        if (id is None):
            return

        id = int(id)
        # Convert to object for DB
        c = Course(ID=id)
        # Get data out of DB
        table = allRecords(self.db.con.cursor(), c)
        # Get data for specific ID
        table = findID(table, id)

        c.storeLookup(Course(
            table[1],  # Course Name
            table[2],  # Course level
            table[0]  # Course ID
        ))

        clear()
        if (c.ID is None):
            print("There is no record for this course ID")
        # Prints current info for ID
        printMenu(c.printInfo())

        return c

    def viewCourses(self):
        msg = {
            "1": "Course ID lookup",
            "2": "View all Courses",
            "q": "Go Back"
        }
        while True:
            out = multiMenu(msg)

            match out:
                case "1":
                    self.printCourse("view")
                    # Wait for user to return to menu
                    input("Press enter to return.")
                case "2":
                    self.viewAllCourses()
                    input("Press enter to return.")
                # Exit case
                case "q": return

    def delCourse(self):
        # Get ID and print for confirmation
        # then save object it to c
        c = self.printCourse("delete")

        choice = yn()
        # If correct, get DB to drop
        if (choice == "y"):
            self.db.delFromDB(c)
        # Any other case, just go to last menu
        return

    def courseMenu(self) -> None:
        msg = {
            "a": "Add Course",
            "r": "Remove Course",
            "e": "Edit Course",
            "v": "View Courses",
            "q": "Go Back"
        }
        # Process kb interupt
        try:
            while True:
                out = multiMenu(msg)

                match out:
                    case "a":
                        c = self.addCourse()
                        if (c is not None):
                            self.db.saveToDB(c)
                    case "r": self.delCourse()
                    case "e":
                        # Call editCourse with the c out from printCourse
                        # this allows the user to confirm inputted ID
                        self.editCourse(self.printCourse("edit"))
                    case "v": self.viewCourses()
                    # Exit case
                    case "q": raise KeyboardInterrupt
        except KeyboardInterrupt:
            return

    def viewAllCourses(self):
        # Sort records by ID number accending
        IDsort = sortListsByID(allRecords(
            self.db.con.cursor(),
            Course()
        ))
        msg = [
            "ID",
            "Course Name",
            "Level"
        ]
        printObj(IDsort, msg)
