from modules import obj


class lookupClass:
    def __init__(self, con) -> None:
        self.con = con

    def student(self) -> list[obj.Student]:
        cur = self.con.cursor()
        # Get student from db
        out = cur.execute("SELECT * FROM Students")

        