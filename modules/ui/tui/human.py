from modules.ui.tui.menus import getInfo, printMenu, clear, yn, multiMenu
from modules.ui.checkers import checkName, checkEmail
from modules.obj import Student, Teacher, Human


class human:
    def addHuman(self) -> Human | None:
        info = getInfo({
            "Please enter the first name.": checkName,
            "Please enter the last name.": checkName,
            "Please enter the middle name.": checkName,
            "Please enter the chosen name.": checkName,
            "Please enter the email.": checkEmail
        })
        # Return if exited by user using kb interupt
        if (info[0] is None):
            return

        p = Human(
            info[0],  # First Name
            info[2],  # Middle Name
            info[1],  # Last Name
            info[3],  # Chosen Name
            info[4]  # Email
        )

        clear()
        printMenu(p.printInfo())
        choice = yn()
        # If correct, return the object
        if (choice == "y"):
            return p
        # Any other case, just go to last menu
        return

    def editHuman(self, p: Student | Teacher) -> None:
        # Handle kb interupt
        if (p is None):
            return
        if (p.ID is None):
            input("Please press enter to continue.")
            return

        # Confirm correct student, otherwise go back a menu
        choice = yn()
        if (choice == "n"):
            return

        msg = {
            "1": "Edit First Name",
            "2": "Edit Middle Name",
            "3": "Edit Last Name",
            "4": "Edit Chosen Name",
            "5": "Edit Email",
            "q": "Go Back"
        }
        choice2 = multiMenu(msg)  # which field to edit
        match choice2:
            case "1":
                p.firstName = getInfo(
                    {f"Editing First Name: {p.firstName}": checkName}
                )[0]
            case "2":
                p.middleName = getInfo(
                    {f"Editing Middle Name: {p.middleName}": checkName}
                )[0]
            case "3":
                p.lastName = getInfo(
                    {f"Editing Last Name: {p.lastName}": checkName}
                )[0]
            case "4":
                p.chosenName = getInfo(
                    {f"Editing Chosen Name: {p.chosenName}": checkName}
                )[0]
            case "5":
                p.email = getInfo(
                    {f"Editing Email: {p.email}": checkEmail}
                )[0]
            case "q": return

        clear()
        # Confirm new info
        printMenu(p.printInfo())
        choice = yn()
        if (choice == "n"):
            return

        # Update the db with the new information
        self.db.updateDB(p)
