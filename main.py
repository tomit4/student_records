import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="rootpassword")

cursor = conn.cursor()

cursor.execute("CREATE DATABASE employee_db")
conn.close()
