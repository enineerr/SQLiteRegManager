import sqlite3
from os import chdir, mkdir
from os import path as osPath


class DB:
    def getWD():
        # Get the "modules" directory
        path = osPath.dirname(__file__)
        # Get the ../modules directory
        path = osPath.dirname(path)
        # Join data to path
        path = osPath.join(path, "data")

        # DEBUG remove line before running
        # reason: vscode debugpy doesnt seem to like paths being passed to args...
        path = osPath.normpath("/home/user/data/")

        return path

    def __init__(self, dbDir: osPath = getWD()):
        # Make sure data folder exists
        # TODO setup try except in case the containing directory doesnt exist,
        # and to prompt the user to correct this.
        if osPath.isdir(dbDir) is False:
            mkdir(dbDir)

        # Set directory to data folder
        chdir(dbDir)

        # Connect to the main db file
        self.con = sqlite3.connect("sql.db")
        # Create cursor
        self.cur = self.con.cursor()

        self.initDB()

        self.cur.close()

        # Close db safely
        self.con.close()

    def initDB(self):
        self.cur.execute("""\
CREATE TABLE IF NOT EXISTS Students (
StudentID   INTEGER PRIMARY KEY,
FirstName    TEXT,
MiddleName   TEXT,
LastName TEXT,
ChosenName  TEXT,
Email   TEXT)
""")
        self.cur.execute("""\
CREATE TABLE IF NOT EXISTS StudentCourseRegistrations (
StudentID   INTEGER,
CourseID    INTEGER,
ResgistrationTime   INTEGER)
""")
        self.cur.execute("""\
CREATE TABLE IF NOT EXISTS Courses (
CourseID   INTEGER PRIMARY KEY,
CourseName  TEXT,
Level   INTEGER)
""")
        self.cur.execute("""\
CREATE TABLE IF NOT EXISTS TeacherCourseRegistrations (
TeacherID   INTEGER,
CourseID    INTEGER,
ResgistrationTime   INTEGER)
""")
        self.cur.execute("""\
CREATE TABLE IF NOT EXISTS Teachers (
TeacherID   INTEGER PRIMARY KEY,
FirstName    TEXT,
MiddleName   TEXT,
LastName TEXT,
ChosenName  TEXT,
Email   TEXT)
""")
        self.con.commit()
