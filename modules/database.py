import sqlite3
from os import chdir
from pathlib import Path
from modules import obj


class DB:
    @staticmethod
    def __getWD() -> Path:
        # Get the "modules" directory
        path = Path(__file__)
        # Get the ../modules directory
        path = path.parent
        # Join data to path
        # path = path.join(path, "data")
        path = path.joinpath("data")

        # DEBUG remove line before running
        # reason: vscode debugpy doesnt seem to like paths being passed to args...
        path = Path("C:\\Users\\User\\Desktop\\Data")

        return path

    def __init__(self, dbDir: Path = __getWD()):
        # Make sure data folder exists
        # TODO setup try except in case the containing directory doesnt exist,
        # and to prompt the user to correct this.
        if dbDir.is_dir() is False:
            dbDir.mkdir()

        # Set directory to data folder
        chdir(dbDir)

        # Connect to the main db file
        self.con = sqlite3.connect("sql.db")
        # Create cursor
        # self.cur = self.con.cursor()

        self.initDB()

        # self.cur.close()

    # Setup DB file with all needed tables
    def initDB(self):
        cur = self.con.cursor()
        cur.execute("""\
CREATE TABLE IF NOT EXISTS Students (
StudentID   INTEGER PRIMARY KEY AUTOINCREMENT,
FirstName    TEXT,
MiddleName   TEXT,
LastName TEXT,
ChosenName  TEXT,
Email   TEXT)
""")
        cur.execute("""\
CREATE TABLE IF NOT EXISTS StudentCourseRegistrations (
StudentID   INTEGER,
CourseID    INTEGER,
ResgistrationTime   INTEGER,
FOREIGN KEY(StudentID) REFERENCES Students(StudentID))
""")
        cur.execute("""\
CREATE TABLE IF NOT EXISTS Courses (
CourseID   INTEGER PRIMARY KEY AUTOINCREMENT,
CourseName  TEXT,
Level   INTEGER)
""")
        cur.execute("""\
CREATE TABLE IF NOT EXISTS TeacherCourseRegistrations (
TeacherID   INTEGER,
CourseID    INTEGER,
ResgistrationTime   INTEGER,
FOREIGN KEY(TeacherID) REFERENCES Teachers(TeacherID))
""")
        cur.execute("""\
CREATE TABLE IF NOT EXISTS Teachers (
TeacherID   INTEGER PRIMARY KEY AUTOINCREMENT,
FirstName    TEXT,
MiddleName   TEXT,
LastName TEXT,
ChosenName  TEXT,
Email   TEXT)
""")
        cur.close()
        self.con.commit()

    def saveToDB(self, DBObject: obj.Student | obj.Teacher | obj.Course) -> None:
        cur = self.con.cursor()
        match type(DBObject):
            case obj.Student:
                cur.execute(f"""\
INSERT INTO Students (
"FirstName",
"MiddleName",
"LastName",
"ChosenName",
"Email")
VALUES (
"{DBObject.firstName}",
"{DBObject.middleName}",
"{DBObject.lastName}",
"{DBObject.chosenName}",
"{DBObject.email}")
""")
            case obj.Teacher:
                pass
            case obj.Course:
                pass

        cur.close()
        self.con.commit()

    def lookupStudentDB(self, ID: int) -> obj.Student:
        cur = self.con.cursor()
        # Get student from db
        out = cur.execute(f"""\
SELECT * FROM Students
WHERE StudentID="{ID}"
""")
        # Get student from output
        out = out.fetchone()

        # Clean up
        cur.close()
        self.con.commit()

        # Convert to student object
        out = obj.Student(obj.Human(
            out[1],  # First name
            out[2],  # Middle Name
            out[3],  # Last Name
            out[4],  # Chosen Name
            out[5],  # Email
            out[0]  # ID number
        ))
        return out

    def delFromDB(self, DBObject: obj.Student | obj.Teacher | obj.Course) -> None:
        # If ID isnt provided, don't try anything
        if (DBObject.ID is None):
            return

        cur = self.con.cursor()

        match type(DBObject):
            case obj.Student:
                cur.execute(f"""\
DELETE FROM Students WHERE StudentID={DBObject.ID}
""")
            case obj.Teacher:
                pass
            case obj.Course:
                pass

        # Clean up
        cur.close()
        self.con.commit()

    # def registerToDB(self, DBObject: Student | Teacher, course: Course) -> None:
    #     match type(DBObject):
    #         case Student:
    #             pass
    #         case Teacher:
    #             pass

    # def unregisterToDB(self, DBObject: Student | Teacher, course: Course) -> None:
    #     match type(DBObject):
    #         case Student:
    #             pass
    #         case Teacher:
    #             pass

    def close(self):
        # Close db safely
        self.con.close()
