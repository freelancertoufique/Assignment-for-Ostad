import json
#=======================Creating a Class with the name of Person=============================
class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

#==================Creating a method with for displaying person Information========================
 
    def display_person_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")

#==========================Creating a new class with the name of Student===========================

class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []


#=========================Creating a method for Adding Grade for a student=========================

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

#=========================Creating a method for how many  courses are available====================

    def enroll_course(self, course_code):
        if course_code not in self.courses:
            self.courses.append(course_code)


#======================Creating a method for displaying student information========================

    def display_student_info(self):
        self.display_person_info()
        print(f"ID: {self.student_id}")
        print(f"Enrolled Courses: {', '.join(self.courses) if self.courses else 'None'}")
        print(f"Grades: {self.grades if self.grades else 'None'}")


#=======================Creating A Class for Courses ============================

class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

#=====================Creating a method for adding student in a course==========================

    def add_student(self, student_id):
        if student_id not in self.students:
            self.students.append(student_id)

#==================Creating A Method for Displaying Course Information=========================

    def display_course_info(self, students_dict):
        print(f"Course Name: {self.course_name}")
        print(f"Code: {self.course_code}")
        print(f"Instructor: {self.instructor}")
        enrolled_names = [students_dict[sid].name for sid in self.students if sid in students_dict]
        print(f"Enrolled Students: {', '.join(enrolled_names) if enrolled_names else 'None'}")

#=====================Creating A new class for Student Management and Course Management===================

class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.courses = {} 

#==========================Adding Student in Students Dictionary===============================

    def add_student(self, name, age, address, student_id):
        if student_id in self.students:
            print("Student ID already exists.")
            return 
        self.students[student_id] = Student(name, age, address, student_id)
        print(f"Student {name} (ID: {student_id}) added successfully.")

#==========Adding course in Courses Dictionary It will show how many Courses are running============

    def add_course(self, course_name, course_code, instructor):
        if course_code in self.courses:
            print("Course code already exists.")
            return
        self.courses[course_code] = Course(course_name, course_code, instructor)
        print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")

#===============This Method is for Enrolling student in a Course=================

    def enroll_student_in_course(self, student_id, course_code):
        if student_id not in self.students:
            print("Invalid student ID.")
            return
        if course_code not in self.courses:
            print("Invalid course code.")
            return
        student = self.students[student_id]
        course = self.courses[course_code]
        student.enroll_course(course_code)
        course.add_student(student_id)
        print(f"Student {student.name} enrolled in {course.course_name}.")

#===================Adding grade for a student =================

    def add_grade_for_student(self, student_id, course_code, grade):
        if student_id not in self.students:
            print("Invalid student ID.")
            return
        if course_code not in self.courses:
            print("Invalid course code.")
            return
        student = self.students[student_id]
        if course_code not in student.courses:
            print("Student is not enrolled in this course.")
            return
        student.add_grade(self.courses[course_code].course_name, grade)
        print(f"Grade {grade} added for {student.name} in {self.courses[course_code].course_name}.")

#==========================Displaying Student Details=========================

    def display_student_details(self, student_id):
        if student_id not in self.students:
            print("Invalid student ID.")
            return
        print("Student Information:")
        self.students[student_id].display_student_info()

#========================for Displaying Course Details==========================

    def display_course_details(self, course_code):
        if course_code not in self.courses:
            print("Invalid course code.")
            return
        print("Course Information:")
        self.courses[course_code].display_course_info(self.students)

#=============================This is a function it will save all the information about Student and Courses in a file name student_management_system as json=============

    def save_data(self, filename="student_management_data.json"):
        data = {
            "students": {
                sid: {
                    "name": s.name,
                    "age": s.age,
                    "address": s.address,
                    "student_id": s.student_id,
                    "grades": s.grades,
                    "courses": s.courses
                } for sid, s in self.students.items()
            },
            "courses": {
                cid: {
                    "course_name": c.course_name,
                    "course_code": c.course_code,
                    "instructor": c.instructor,
                    "students": c.students
                } for cid, c in self.courses.items()
            }
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("All student and course data saved successfully.")

    def load_data(self, filename="student_management_data.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.students = {}
            for sid, s in data.get("students", {}).items():
                student = Student(s["name"], s["age"], s["address"], s["student_id"])
                student.grades = s["grades"]
                student.courses = s["courses"]
                self.students[sid] = student
            self.courses = {}
            for cid, c in data.get("courses", {}).items():
                course = Course(c["course_name"], c["course_code"], c["instructor"])
                course.students = c["students"]
                self.courses[cid] = course
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No saved data found.")
#===============cli information is here================
def main():
    sms = StudentManagementSystem()
    while True:
        print("\n==== Student Management System ====")
        print("1. Add New Student")
        print("2. Add New Course")
        print("3. Enroll Student in Course")
        print("4. Add Grade for Student")
        print("5. Display Student Details")
        print("6. Display Course Details")
        print("7. Save Data to File")
        print("8. Load Data from File")
        print("0. Exit")
        choice = input("Select Option: ").strip()
        if choice == "1":
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            address = input("Enter Address: ")
            student_id = input("Enter Student ID: ")
            sms.add_student(name, age, address, student_id)
        elif choice == "2":
            course_name = input("Enter Course Name: ")
            course_code = input("Enter Course Code: ")
            instructor = input("Enter Instructor: ")
            sms.add_course(course_name, course_code, instructor)
        elif choice == "3":
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            sms.enroll_student_in_course(student_id, course_code)
        elif choice == "4":
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            grade = input("Enter Grade: ")
            sms.add_grade_for_student(student_id, course_code, grade)
        elif choice == "5":
            student_id = input("Enter Student ID: ")
            sms.display_student_details(student_id)
        elif choice == "6":
            course_code = input("Enter Course Code: ")
            sms.display_course_details(course_code)
        elif choice == "7":
            sms.save_data()
        elif choice == "8":
            sms.load_data()
        elif choice == "0":
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.") # if we use the number less than 0 and greater than 8 it will say Invalid option Please Try again.

if __name__ == "__main__":
    main()