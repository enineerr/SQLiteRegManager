import sqlite3
from os import chdir
from pathlib import Path
from modules import obj
from modules.database.lookup import getTable


class DB():
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
Email   TEXT UNIQUE)
""")
        cur.execute("""\
CREATE TABLE IF NOT EXISTS StudentRegistrations (
RegistrationID   INTEGER PRIMARY KEY AUTOINCREMENT,
StudentID   INTEGER,
CourseID    INTEGER,
RegistrationTime   TIMESTAMP,
UNIQUE(StudentID, CourseID),
FOREIGN KEY(CourseID) REFERENCES Courses(CourseID),
FOREIGN KEY(StudentID) REFERENCES Students(StudentID))
""")
        cur.execute("""\
CREATE TABLE IF NOT EXISTS Courses (
CourseID   INTEGER PRIMARY KEY AUTOINCREMENT,
CourseName  TEXT,
Level   INTEGER)
""")
        cur.execute("""\
CREATE TABLE IF NOT EXISTS TeacherRegistrations (
RegistrationID   INTEGER PRIMARY KEY AUTOINCREMENT,
TeacherID   INTEGER,
CourseID    INTEGER,
RegistrationTime   TIMESTAMP,
UNIQUE(TeacherID, CourseID),
FOREIGN KEY(CourseID) REFERENCES Courses(CourseID),
FOREIGN KEY(TeacherID) REFERENCES Teachers(TeacherID))
""")
        cur.execute("""\
CREATE TABLE IF NOT EXISTS Teachers (
TeacherID   INTEGER PRIMARY KEY AUTOINCREMENT,
FirstName    TEXT,
MiddleName   TEXT,
LastName TEXT,
ChosenName  TEXT,
Email   TEXT UNIQUE)
""")
        cur.close()
        self.con.commit()

    def saveToDB(
            self,
            DBObject: obj.Student | obj.Teacher | obj.Course | obj.sReg | obj.tReg
    ) -> None:
        cur = self.con.cursor()

        table = getTable(DBObject)

        # takes col names twice, adds "=:" between them
        # then separates each with ", "
        # ex. ":FirstName, ..."
        places = ", ".join(
            map(
                lambda a: f":{a}", table[2]
            )
        )

        cols = ", ".join(table[2])

        values = DBObject.saveValues()

        try:
            cur.execute(
                f"INSERT INTO {table[0]} ({cols}) VALUES ({places})",
                (values)
            )
        # Only reason this would happen is duplicate email addresses
        except sqlite3.IntegrityError:
            raise ValueError("Record already registered")
        finally:
            # Clean up
            cur.close()
            self.con.commit()

    # def delFromDB(self, DBObject: obj.Student | obj.Teacher | obj.Course) -> None:
    def delFromDB(
            self,
            DBObject: obj.Student | obj.Teacher | obj.Course | obj.sReg | obj.tReg
    ) -> None:
        # If ID isnt provided, don't try anything
        if (DBObject.ID is None):
            return

        cur = self.con.cursor()

        table = getTable(DBObject)

        cur.execute(
            f"DELETE FROM {table[0]} WHERE {table[1]}=?",
            (str(DBObject.ID))
        )
        # Clean up
        cur.close()
        self.con.commit()

    # def updateDB(self, DBObject: obj.Student | obj.Teacher | obj.Course) -> None:
    def updateDB(
            self,
            DBObject: obj.Student | obj.Teacher | obj.Course | obj.sReg | obj.tReg
    ) -> None:
        table = getTable(DBObject)

        values = DBObject.saveValues()

        # takes col names twice, adds "=:" between them
        # then separates each with ", "
        # ex. "FirstName=:FirstName, ..."
        places = ", ".join(
            map(
                lambda a, b: f"{a}=:{b}", table[2], table[2]
            )
        )

        cur = self.con.cursor()
        # Update DB record
        cur.execute(
            f"UPDATE {table[0]} SET {places} WHERE {table[1]}={DBObject.ID}",
            (values)
        )
        # Clean up
        cur.close()
        self.con.commit()

    def close(self):
        # Close db safely
        self.con.close()
