class Course():
    # def __init__(self) -> None:
    #     pass
    def __init__(
            self,
            courseName: str | None = "",
            level: int | None = None,
            ID: int | None = None
    ):
        self.courseName = courseName
        self.level = level
        self.ID = ID

    def printInfo(self) -> dict[str, str]:
        msg = {
            "Course Name": self.courseName,
            "Level": self.level,
            "ID": self.ID
        }
        # Remove ID if it is empty
        if (self.ID is None):
            msg.pop("ID")

        # return info for printing/use
        return msg

    def storeLookup(self, out):
        self.courseName = out.courseName
        self.level = out.level
        self.ID = out.ID  # This *should* never do anything

    def saveValues(self) -> str:
        return f"""\
"{self.courseName}",
"{self.level}")
"""

    def updateValues(self) -> str:
        return f"""
CourseName =      "{self.courseName}",
Level =    "{self.level}"
"""
