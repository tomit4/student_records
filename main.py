import re
import sqlite3
import sys


def display_menu():
    print("========================================")
    print("=========== STUDENT DATABASE ===========")
    print("========================================")
    print("OPTIONS:")
    print("1) READ THE DATABASE")
    print("2) WRITE A RECORD TO THE DATABASE")
    print("3) UPDATE A DATABASE RECORD")
    print("4) DELETE A DATABASE RECORD")
    print("5) QUIT THE PROGRAM")


def get_user_input():
    while True:
        try:
            user_choice = int(input("Please enter your choice: "))
            if user_choice >= 1 and user_choice <= 5:
                return user_choice
            else:
                print("Sorry, you can only select numbers between 1 and 5.")
                print("Please try again.")
                continue
        except ValueError:
            print("Sorry, that's not a number. Please try again")
            continue


def create_students_table(con):
    try:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                grade TEXT NOT NULL,
                email TEXT NOT NULL)
            """)
        cur.close()
    except sqlite3.OperationalError as e:
        print("Failed to create table in database:", e)


########################
# READ LOGIC
#######################
def display_students(con):
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
        cur.close()
        return list(rows)
    except sqlite3.OperationalError as e:
        print("Failed to select all rows from students table: ", e)


########################
# INSERT LOGIC
#######################
def prompt_for_insert_data():
    while True:
        first_name = input("Enter student first name: ")
        if is_valid_name(first_name):
            break
        print("Invalid first name. User letters only.")

    while True:
        last_name = input("Enter student last name: ")
        if is_valid_name(last_name):
            break
        print("Invalid last name. User letters only.")

    while True:
        grade = input("Enter grade (A, B, C, D, F): ").upper()
        if is_valid_grade(grade):
            break
        print("Invalid grade.")

    while True:
        email = input("Enter email: ")
        if is_valid_email(email):
            break
        print("Invalid email format.")

    name = first_name + " " + last_name
    return name, grade, email


def insert_student_data(con, name, grade, email):
    try:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO students(name, grade, email) VALUES (?, ?, ?)",
            (name, grade, email),
        )
        con.commit()
        cur.close()
        print("Successfully added new student!")
    except sqlite3.OperationalError as e:
        print("Failed to insert data into students table: ", e)


########################
# UPDATE LOGIC
#######################


def prompt_for_update_data(con):
    while True:
        student_id = prompt_for_student_id("to update")
        id_exists = id_is_in_database(con, student_id)
        if id_exists:
            update_fields = prompt_for_update_fields(con, student_id)
            update_student(con, student_id, update_fields)
            break
        else:
            print(f"{student_id} is not in the students database, please try again")
            continue


def prompt_for_update_fields(con, student_id):
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        rows = cur.fetchall()
        while True:
            pretty_print(rows)
            update_fields = (
                input(
                    "Enter fields you wish to update for student (name, grade, email),\nSeparate each field by a space: "
                )
                .lower()
                .split(" ")
            )
            for field in update_fields:
                if not is_valid_field(field):
                    print(f"{field} is not a valid field, please try again")
                    continue
                else:
                    cur.close()
                    return update_fields
    except sqlite3.OperationalError as e:
        print("Failed to select ids from students table: ", e)


def update_student(con, student_id, update_fields):
    new_values = {}

    for field in update_fields:
        if field == "name":
            while True:
                first_name = input("Enter new first name: ")
                if is_valid_name(first_name):
                    break
                print("Invalid first name. Use letters only.")

            while True:
                last_name = input("Enter new last name: ")
                if is_valid_name(last_name):
                    break
                print("Invalid last name. Use letters only.")

            new_values["name"] = first_name + " " + last_name

        elif field == "grade":
            while True:
                grade = input("Enter new grade (A, B, C, D, F): ").upper()
                if is_valid_grade(grade):
                    break
                print("Invalid grade.")
            new_values["grade"] = grade

        elif field == "email":
            while True:
                email = input("Enter new email: ")
                if is_valid_email(email):
                    break
                print("Invalid email format.")
            new_values["email"] = email

    set_clause = ", ".join(f"{field} = ?" for field in new_values.keys())
    values = tuple(new_values.values()) + (student_id,)

    try:
        cur = con.cursor()
        cur.execute(f"UPDATE students SET {set_clause} WHERE id = ?", values)
        con.commit()
        print("Successfully updated student!")
        cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        rows = cur.fetchall()
        pretty_print(rows)
        cur.close()
    except sqlite3.OperationalError as e:
        print("Failed to update students table: ", e)


########################
# DELETE LOGIC
#######################


def prompt_for_delete_data(con):
    while True:
        print("WARNING: You are about to delete a student's record from the database!")
        print("Student Records cannot be restored after deletion!")
        are_you_sure = input(
            "Are you sure you wish to delete a student's record? (y/n): "
        ).lower()
        if are_you_sure in ["y", "yes"]:
            break
        elif are_you_sure in ["n", "no"]:
            return
        else:
            print("Please enter 'y' or 'n' to confirm.")
            continue
    while True:
        student_id = prompt_for_student_id("to delete")
        id_exists = id_is_in_database(con, student_id)

        if id_exists:
            try:
                cur = con.cursor()
                cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
                rows = cur.fetchall()
                pretty_print(rows)
                cur.close()
            except sqlite3.OperationalError as e:
                print("Failed to select student from students table: ", e)
            are_you_really_sure = input(
                f"Are you sure you wish to delete student with id {student_id}? (y/n): "
            ).lower()
            if are_you_really_sure in ["y", "yes"]:
                delete_student(con, student_id)
                break
            else:
                return
        else:
            print(f"{student_id} is not in the students database, please try again.")
            continue


def delete_student(con, student_id):
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
        con.commit()
        print("Successfully deleted student!")
        cur.close()
    except sqlite3.OperationalError as e:
        print("Failed to delete from students table: ", e)


########################
# HELPER FUNCTIONS
#######################
def is_valid_name(name):
    return name.isalpha()


def is_valid_grade(grade):
    return grade.upper() in ["A", "B", "C", "D", "F"]


def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


def is_valid_field(field):
    return field in ["name", "grade", "email"]


def prompt_for_student_id(to_phrase):
    student_id = None
    while True:
        try:
            student_id = int(input(f"Enter ID of student {to_phrase} : "))
            break
        except ValueError:
            print("Please enter a valid integer ID.")
    if student_id:
        return student_id


def pretty_print(rows):
    print("\nID  Name                 Grade  Email")
    print("------------------------------------------------------------")

    for row in rows:
        id, name, grade, email = row
        print(f"{id:<3} {name:<20} {grade:<6} {email}")

    print()


def id_is_in_database(con, student_id):
    try:
        cur = con.cursor()
        cur.execute("SELECT id FROM students")
        rows = cur.fetchall()
        ids = [row[0] for row in rows]
        cur.close()
        return student_id in ids
    except sqlite3.OperationalError as e:
        print("Failed to select ids from students table: ", e)


def insert_dummy_data(con):
    try:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM students")
        count = cur.fetchone()[0]
        if count == 0:
            dummy_students = [
                ("Alice Johnson", "A", "alice.johnson@example.com"),
                ("Bob Smith", "B", "bob.smith@example.com"),
                ("Carol Lee", "C", "carol.lee@example.com"),
                ("David Brown", "B", "david.brown@example.com"),
            ]
            cur.executemany(
                "INSERT INTO students(name, grade, email) VALUES (?, ?, ?)",
                dummy_students,
            )
            con.commit()
        cur.close()
    except sqlite3.OperationalError as e:
        print("Failed to insert dummy data:", e)


########################
# MAIN LOOP
#######################
def main(con):
    while True:
        display_menu()
        user_choice = get_user_input()
        match user_choice:
            case 1:
                rows = display_students(con)
                pretty_print(rows)
            case 2:
                name, grade, email = prompt_for_insert_data()
                insert_student_data(con, name, grade, email)
            case 3:
                prompt_for_update_data(con)
            case 4:
                prompt_for_delete_data(con)
            case 5:
                print("Goodbye!")
                break
            case _:
                continue


if __name__ == "__main__":
    con = None
    try:
        with sqlite3.connect("students.db") as con:
            create_students_table(con)
            insert_dummy_data(con)
            main(con)
    except sqlite3.Error as e:
        print("Failed to connect to database: ", e)
    finally:
        if con:
            con.close()
        sys.exit()
