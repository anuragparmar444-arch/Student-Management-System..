import sqlite3

DATABASE_NAME = "students.db"


def connect_db():
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll_no INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age > 0),
                course TEXT NOT NULL,
                marks REAL NOT NULL CHECK(marks >= 0 AND marks <= 100)
            )
        """)


def add_student():
    try:
        roll_no = int(input("Enter Roll Number: "))
        name = input("Enter Student Name: ").strip()
        age = int(input("Enter Age: "))
        course = input("Enter Course: ").strip()
        marks = float(input("Enter Marks (0-100): "))

        if not name or not course:
            print("Error: Name and course cannot be empty.")
            return
        if age <= 0 or not 0 <= marks <= 100:
            print("Error: Age must be positive and marks must be between 0 and 100.")
            return

        with connect_db() as conn:
            conn.execute("""
                INSERT INTO students (roll_no, name, age, course, marks)
                VALUES (?, ?, ?, ?, ?)
            """, (roll_no, name, age, course, marks))
        print("Student added successfully!")

    except sqlite3.IntegrityError:
        print("Error: This Roll Number already exists.")
    except ValueError:
        print("Error: Please enter valid numbers for roll number, age, and marks.")


def view_students():
    with connect_db() as conn:
        students = conn.execute("""
            SELECT roll_no, name, age, course, marks
            FROM students ORDER BY roll_no
        """).fetchall()

    if not students:
        print("No student records found.")
        return

    print("\n" + "=" * 78)
    print(f"{'ROLL NO.':<10}{'NAME':<22}{'AGE':<7}{'COURSE':<20}{'MARKS':>8}")
    print("-" * 78)
    for roll_no, name, age, course, marks in students:
        print(f"{roll_no:<10}{name[:21]:<22}{age:<7}{course[:19]:<20}{marks:>8.1f}")
    print("=" * 78)


def search_student():
    try:
        roll_no = int(input("Enter Roll Number to Search: "))
        with connect_db() as conn:
            student = conn.execute("""
                SELECT roll_no, name, age, course, marks
                FROM students WHERE roll_no = ?
            """, (roll_no,)).fetchone()

        if student:
            print("\nStudent Found!")
            print(f"Roll Number: {student[0]}")
            print(f"Name       : {student[1]}")
            print(f"Age        : {student[2]}")
            print(f"Course     : {student[3]}")
            print(f"Marks      : {student[4]:.1f}")
        else:
            print("Student not found.")
    except ValueError:
        print("Error: Please enter a valid Roll Number.")


def update_student():
    try:
        roll_no = int(input("Enter Roll Number to Update: "))
        with connect_db() as conn:
            student = conn.execute("""
                SELECT roll_no, name, age, course, marks
                FROM students WHERE roll_no = ?
            """, (roll_no,)).fetchone()

            if student is None:
                print("Student not found.")
                return

            name_input = input(f"Enter New Name [{student[1]}]: ").strip()
            age_input = input(f"Enter New Age [{student[2]}]: ").strip()
            course_input = input(f"Enter New Course [{student[3]}]: ").strip()
            marks_input = input(f"Enter New Marks [{student[4]}]: ").strip()

            name = name_input or student[1]
            age = int(age_input) if age_input else student[2]
            course = course_input or student[3]
            marks = float(marks_input) if marks_input else student[4]

            if age <= 0 or not 0 <= marks <= 100:
                print("Error: Age must be positive and marks must be between 0 and 100.")
                return

            conn.execute("""
                UPDATE students
                SET name = ?, age = ?, course = ?, marks = ?
                WHERE roll_no = ?
            """, (name, age, course, marks, roll_no))
        print("Student updated successfully!")
    except ValueError:
        print("Error: Please enter valid numbers for age and marks.")


def delete_student():
    try:
        roll_no = int(input("Enter Roll Number to Delete: "))
        with connect_db() as conn:
            student = conn.execute(
                "SELECT name FROM students WHERE roll_no = ?", (roll_no,)
            ).fetchone()

            if student is None:
                print("Student not found.")
                return

            confirm = input(f"Delete record of {student[0]}? (yes/no): ").strip().lower()
            if confirm == "yes":
                conn.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
                print("Student deleted successfully!")
            else:
                print("Delete cancelled.")
    except ValueError:
        print("Error: Please enter a valid Roll Number.")


def main():
    create_table()
    while True:
        print("\n" + "=" * 38)
        print("       STUDENT MANAGEMENT SYSTEM")
        print("=" * 38)
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter Your Choice (1-6): ").strip()
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Thank you for using Student Management System!")
            break
        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
