import sqlite3

class Student:

	def __init__(self, StudentID,StudentName):
		self.StudentID = StudentID
		self.StudentName = StudentName
		
	def print_student_details(self):
		print('Student Id:', self.StudentID,' , Student Name:',self.StudentName)

	def print_all_students_details(cursor,connection):
		pass

	def add_new_student(self,cursor,connection):
		cursor.execute("INSERT INTO StudentsCoursesRegistraions (StudentID,StudentName) VALUES (?, ?)", (self.StudentID, self.StudentName))
		connection.commit()
		print('Student Added Successfully')

	def update_student(self,cursor,connection):
		cursor.execute("UPDATE StudentsCoursesRegistraions SET StudentName = ? WHERE StudentID = ", (self.StudentName, self.StudentID))
		connection.commit()
		print('Student Updated Successfully')

	def delete_student(StudentID,cursor,connection):
		cursor.execute("DELETE FROM StudentsCoursesRegistraions WHERE StudentID = ?", (StudentID,))
		connection.commit()
		print('Student Deleted Successfully')		

def create_tables():
	cursor.execute('''CREATE TABLE IF NOT EXISTS StudentsCoursesRegistraions (
						StudentID	INTEGER PRIMARY KEY,
						StudentName	TEXT,
						CourseID	INTEGER,
						Course_Details	TEXT,
						TeacherID	INTEGER,
						Teacher_name	TEXT,
						Registration_Date	TEXT)''')
	connection.commit()


def main_menu():
    print('what would you like to manage:\n press 1 for Students,\n 2 for teachers,\n 3 for courses,\n 4 for enrollment')
    choice = input('Input your choice: ')
    if  choice == '1':
        print('\n\nYou have chosen Student Management,\n press 1 to add a new student,\n 2 to update an exsiting student,\n 3 to delete a student,\n 4 to view all students details')
        student_management_choice = input('Input your choice: ')
        if  student_management_choice == '1':
             StudentID = input('input student id: ')
             StudentName = input('input student name: ')
             s = Student(StudentID,StudentName)
             s.add_new_student(cursor,connection)
             s.print_student_details()
        elif student_management_choice == '2':
             StudentID = input('Which student detail you want to update: input student id: ')
             StudentName = input('input an updated student name: ')
             s = Student(StudentID,StudentName)
             s.update_student(cursor,connection)
             s.print_student_details()
        elif student_management_choice == '3':
            Student.delete_student(1,cursor,connection)
        elif student_management_choice == '4':
            Student.print_all_students_details(cursor,connection)
        else:
            print('input is not valid')

connection = sqlite3.connect('school.db')
cursor = connection.cursor()
create_tables()
main_menu()
connection.close()