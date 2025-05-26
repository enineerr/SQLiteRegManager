from modules import obj
import sqlite3


@staticmethod
def oneRecord(cur, DBObject: obj.Student | obj.Teacher | obj.Course) -> obj.Human | obj.Course:
    table = getTable()

    # Get student from db
    out = cur.execute(f"""\
SELECT * FROM {table[0]}
WHERE {table[1]}="{DBObject.ID}"
""")
    # Get student from output
    out = out.fetchone()

    # Clean up
    cur.close()

    if (type(DBObject) is obj.Course):
        # do course handling and return
        pass

    # Convert to human object
    # if ID was invalid:
    if (out is None):
        out = obj.Human()
    # if ID was valid:
    else:
        out = obj.Human(
            out[1],  # First name
            out[2],  # Middle Name
            out[3],  # Last Name
            out[4],  # Chosen Name
            out[5],  # Email
            out[0]  # ID number
        )

    return out


@staticmethod
# def allRecords(cur, DBObject: type[obj.Student] | obj.Teacher | obj.Course) -> list[obj.Human] | list[obj.Course]:
def allRecords(
    cur,
    DBObject: obj.Student | obj.Teacher | obj.Course
) -> list[list[str | int]]:

    table = getTable(DBObject)

    # Get student from db
    out = cur.execute(f"""\
SELECT * FROM {table[0]}
""")
    # Get student from output
    out = out.fetchall()

    # Clean up
    cur.close()

    if (type(DBObject) is obj.Course):
        # do course handling and return
        pass

    # Convert to human object
    # if ID was invalid:
    if (out is None):
        listOut = [[""]]
    # if ID was valid:
    else:
        listOut = []
        for i in out:
            listOut.append(
                [
                    i[0],  # ID number
                    i[1],  # First name
                    i[2],  # Middle Name
                    i[3],  # Last Name
                    i[4],  # Chosen Name
                    i[5]  # Email
                ]
            )

    return listOut


@staticmethod
def getTable(DBObject: obj.Student | obj.Teacher | obj.Course) -> list[str]:
    match type(DBObject):
        case obj.Student: table = ["Students", "StudentID"]
        case obj.Teacher: table = ["Teachers", "TeacherID"]
        case obj.Course: table = ["Courses", "CourseID"]

    return table
