import re
import sqlite3
import sys


def display_menu():
    """Print the main menu options to the console"""
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
    """
    Prompt the user to select a menu option.

    Returns:
        int: A valid menu choice between 1 and 5.
    """
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


########################
# DATABASE SETUP
#######################
def create_students_table(con):
    """
    Create the 'students' table if it does not exist.

    Args:
        con (sqlite3.Connection): The database connection object.
    """
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
    except sqlite3.Error as e:
        print("A generic database error occured: ", e)


########################
# READ LOGIC
#######################
def display_students(con):
    """
    Reads and outputs all rows from the 'students' table.

    Args:
        con (sqlite3.Connection): The database connection object.
    Returns:
        list (tuple): A list of all rows from the students table.
    """
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
        cur.close()
        return list(rows)
    except sqlite3.OperationalError as e:
        print("Failed to select all rows from students table: ", e)
    except sqlite3.Error as e:
        print("A generic database error occured: ", e)


########################
# INSERT LOGIC
#######################
def prompt_for_insert_data():
    """
    Presents a series of prompts for student data
    to be inserted into 'students' table.

    Returns:
        list (str): A list of the entered name, grade, and email strings.
    """
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
    """
    Inserts new student record into `students` table

    Args:
        con (sqlite3.Connection): The database connection object.
        name: the student's name string
        grade: the student's grade string
        email: the student's email string
    """
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
    except sqlite3.Error as e:
        print("A generic database error occured: ", e)


########################
# UPDATE LOGIC
#######################


def prompt_for_update_data(con):
    """
    Prompts the user for which student id they wish to update and updates fields accordingly

    Args:
        con (sqlite3.Connection): The database connection object.
    """
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
    """
    Presents a series of prompts asking the user for
    which fields they wish to update (name, grade, email)

    Args:
        con (sqlite3.Connection): The database connection object.
        student_id (int): The student's id
    Returns:
        list (str): A list of selected fields to update
    """
    rows = get_student_by_id(con, student_id)
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
                return update_fields


def update_student(con, student_id, update_fields):
    """
    Updates the student's record with the selected new fields.

    Args:
        con (sqlite3.Connection): The database connection object.
        student_id (int): The student's id
        update_fields (list[str]): A list of selected fields to update
    """
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
        cur.close()
        print("Successfully updated student!")
        rows = get_student_by_id(con, student_id)
        pretty_print(rows)
    except sqlite3.OperationalError as e:
        print("Failed to update students table: ", e)
    except sqlite3.Error as e:
        print("A generic database error occured: ", e)


########################
# DELETE LOGIC
#######################


def prompt_for_delete_data(con):
    """
    Prompts the user for a student ID to delete and confirms deletion.

    Args:
        con (sqlite3.Connection): The database connection object.
    """
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
            rows = get_student_by_id(con, student_id)
            pretty_print(rows)
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
    """
    Deletes student record by ID from the 'students' table.

    Args:
        con (sqlite3.Connection): The database connection object.
        student_id (int): The student's id
    """
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
        con.commit()
        print("Successfully deleted student!")
        cur.close()
    except sqlite3.OperationalError as e:
        print("Failed to delete from students table: ", e)
    except sqlite3.Error as e:
        print("A generic database error occured: ", e)


########################
# HELPER FUNCTIONS
#######################
def is_valid_name(name):
    """Check if name contains only letters."""
    return name.isalpha()


def is_valid_grade(grade):
    "Check if grade is one of A, B, C, D, F."
    return grade.upper() in ["A", "B", "C", "D", "F"]


def is_valid_email(email):
    """Check if email has valid format (simple regex)."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


def is_valid_field(field):
    """Check if the field is one of 'name', 'grade', 'email'."""
    return field in ["name", "grade", "email"]


def prompt_for_student_id(to_phrase):
    """
    Generic prompt for specific student id

    Args:
        to_phrase (str): Context for prompt(e.g., 'to update').

    Returns:
        int: Valid student ID.
    """
    student_id = None
    while True:
        try:
            student_id = int(input(f"Enter ID of student {to_phrase} : "))
            break
        except ValueError:
            print("Please enter a valid integer ID.")
    if student_id:
        return student_id


def get_student_by_id(con, student_id):
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        rows = cur.fetchall()
        cur.close()
        return rows
    except sqlite3.OperationalError as e:
        print("Failed to select ids from students table: ", e)
    except sqlite3.Error as e:
        print("A generic database error occured: ", e)


def pretty_print(rows):
    """
    Prints the outputted rows from the 'students' database in a readable format

    Args:
        rows (list[tuple[int, str, str, str]]): rows outputted from the select query
    """
    print("\nID  Name                 Grade  Email")
    print("------------------------------------------------------------")

    for row in rows:
        id, name, grade, email = row
        print(f"{id:<3} {name:<20} {grade:<6} {email}")

    print()


def id_is_in_database(con, student_id):
    """
    Check if a student ID exists in the database.

    Args:
        con (sqlite3.Connection): Database connection.
        student_id (int): ID to check.

    Returns:
        bool: True if ID exists, False otherwise.
    """
    try:
        cur = con.cursor()
        cur.execute("SELECT id FROM students")
        rows = cur.fetchall()
        ids = [row[0] for row in rows]
        cur.close()
        return student_id in ids
    except sqlite3.OperationalError as e:
        print("Failed to select ids from students table: ", e)
    except sqlite3.Error as e:
        print("A generic database error occured: ", e)


def insert_dummy_data(con):
    """
    Insert sample students into the database if the table is empty.

    Args:
        con (sqlite3.Connection): The database connection object.
    """
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
    except sqlite3.Error as e:
        print("A generic database error occured: ", e)


########################
# MAIN LOOP
#######################
def main():
    """Run the menu-driven application."""
    con = None
    try:
        # Use context manager to automatically commit/close
        with sqlite3.connect("students.db") as con:
            create_students_table(con)
            insert_dummy_data(con)
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
    except sqlite3.Error as e:
        print("Failed to connect to database: ", e)
    finally:
        if con:
            con.close()
        sys.exit()


if __name__ == "__main__":
    main()
