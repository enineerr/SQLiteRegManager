from modules import obj
from datetime import datetime


@staticmethod
def getRegistrations(cur, DBObject: obj.sReg | obj.tReg) -> list[list[str | int | datetime]]:
    match type(DBObject):
        case obj.sReg:
            cur.execute("""\
SELECT Students.StudentID, Students.FirstName, Students.LastName, Students.ChosenName,
Courses.CourseID, Courses.CourseName, Courses.Level,
StudentRegistrations.RegistrationTime, StudentRegistrations.RegistrationID
FROM
(
Students RIGHT JOIN  StudentRegistrations ON Students.StudentID=StudentRegistrations.StudentID
LEFT JOIN  Courses ON StudentRegistrations.CourseID = Courses.CourseID
)
""")
        case obj.tReg:
            cur.execute("""\
SELECT Teachers.TeacherID, Teachers.FirstName, Teachers.LastName, Teachers.ChosenName,
Courses.CourseID, Courses.CourseName, Courses.Level,
TeacherRegistrations.RegistrationTime, TeacherRegistrations.RegistrationID
FROM
(
Teachers RIGHT JOIN TeacherRegistrations ON Teachers.TeacherID=TeacherRegistrations.TeacherID
LEFT JOIN Courses ON TeacherRegistrations.CourseID = Courses.CourseID
)
""")

    out = cur.fetchall()
    # Convert to list of human-like objects
    # if ID was invalid:
    if (out == []):
        listOut = [["", "", "", ""]]
    # if table was not empty:
    else:
        listOut = []
        for i in out:
            listOut.append(
                [
                    i[0],  # hID
                    i[1],  # FirstName
                    i[2],  # LastName
                    i[3],  # ChosenName
                    i[4],  # CourseID
                    i[5],  # CourseName
                    i[6],  # Level
                    datetime.fromisoformat(i[7]),  # Reg Time
                    i[8]  # RegistrationID
                ]
            )
    return listOut

@staticmethod
def allRecords(
    cur,
    DBObject: obj.Student | obj.Teacher | obj.Course
) -> list[list[str | int | datetime]]:

    table = getTable(DBObject)

    out = cur.execute(f"SELECT * FROM {table[0]}")

    # Get student from output
    out = out.fetchall()

    # Clean up
    cur.close()

    # For some reason, types won't work here.
    match table[0]:
        case "Courses":
            # Convert to list of course-like objects
            # if table was empty:
            if (out == []):
                listOut = [["", "", ""]]
            else:
                listOut = []
                for i in out:
                    listOut.append(
                        [
                            i[0],  # ID number
                            i[1],  # Course Name
                            i[2]  # Course level
                        ]
                    )
        case "StudentRegistrations" | "TeacherRegistrations":
            # Convert to list of reg-like objects
            # if ID was invalid:
            if (out == []):
                listOut = [["", "", "", ""]]
            # if table was not empty:
            else:
                listOut = []
                for i in out:
                    listOut.append(
                        [
                            i[0],  # ID number
                            i[1],  # Human ID
                            i[2],  # Course ID
                            datetime.fromtimestamp(i[3]),  # Reg Time
                        ]
                    )
        case _:
            # Convert to list of human-like objects
            # if ID was invalid:
            if (out == []):
                listOut = [["", "", "", "", "", ""]]
            # if table was not empty:
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
def getTable(
    DBObject: obj.Student | obj.Teacher | obj.Course | obj.sReg | obj.tReg
) -> list[str | list[str]]:
    match type(DBObject):
        # [0] -> Table Name
        # [1] -> ID Name
        # [2] -> List of columns
        case obj.Student: table = ["Students", "StudentID"]
        case obj.Teacher: table = ["Teachers", "TeacherID"]
        case obj.Course:
            table = [
                "Courses",
                "CourseID",
                [
                    "CourseName",
                    "Level"
                ]
            ]
            # Return now to prevent human Placeholders
            return table
        case obj.sReg:
            table = [
                "StudentRegistrations",
                "RegistrationID",
                [
                    "StudentID",
                    "CourseID",
                    "RegistrationTime"
                ]
            ]
            # Return now to prevent human Placeholders
            return table
        case obj.tReg:
            table = [
                "TeacherRegistrations",
                "RegistrationID",
                [
                    "TeacherID",
                    "CourseID",
                    "RegistrationTime"
                ]
            ]
            # Return now to prevent human Placeholders
            return table

    # Human Placeholders
    table.append([
        "FirstName",
        "MiddleName",
        "LastName",
        "ChosenName",
        "Email"
    ])
    return table
