# Programming In Python - Assigment 2: Database and Record Management

## Introduction

This repository hold's my code for [Study.com](https://study.com)'s Programming
In Python course's Assignment 2: Database and Record Management.

### Prompt

In this assignment, you will create a Python program that allows a user to
manage student records stored in an SQLite database. You'll design a
menu-driven, command-line application that supports all basic CRUD operations.
This assignment focuses on modular design and robust error handling, helping you
build clean, maintainable code that interacts smoothly with a persistent data
layer.

Your program should:

1. Connect to an SQLite database file. If the database does not already exist,
   your program should create it.

2. Define and create a table named students with the following columns: id
   (INTEGER, primary key), name (TEXT), grade (TEXT), and email (TEXT).

3. Provide a simple text-based menu that allows the user to:

   - Add a new student record
   - View all existing student records
   - Update an existing student's information Delete a student record
   - Exit the program

4. Implement each database operation in a separate Python function for clarity
   and reusability.

5. Validate user inputs (e.g., ensure email contains an '@' symbol, ID is an
   integer, prompt user for confirmation before deleting a record).

6. Use try-except blocks to handle possible runtime errors such as failed
   database operations or invalid user input.

7. Ensure all changes are saved persistently in the .db file so that records are
   retained between sessions.

### Grading Rubric

Your output will be graded on the following rubric:

| **Criteria**                              | **Excellent(5)**                                                                                                 |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Database Connection & Table Creation (x3) | Correctly connects to SQLite, creates database if not found, and defines students table with all required fields |
| CRUD Functionality & Menu Navigation (x3) | Fully functional menu with all CRUD operations, each clearly implemented in a separate function                  |
| Input Validation & User Interaction (x2)  | Strong input validation and user interaction; catches invalid inputs and confirms deletes                        |
| Error Handling (try-except) (x2)          | Robust use of try-except blocks to catch and handle likely runtime errors gracefully                             |
| Persistence & File Saving (x3)            | Ensures all changes are committed and persist across sessions; uses connection/commit/close effectively          |
| Code Quality & Modularity (x3)            | Code is modular, readable, well-organized, and documented; adheres to Python conventions                         |
