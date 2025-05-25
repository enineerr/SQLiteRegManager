from pathlib import Path
from modules.database import DB
# from modules.obj import Student, Teacher, Course, Human


class UI:
    def __init__(self, dbpath: Path | None = None):
        if dbpath is None:
            self.db = DB()
        else:
            self.db = DB(dbpath)

    def closeDB(self) -> None:
        self.db.close()
