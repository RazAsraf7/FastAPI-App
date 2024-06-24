import mysql.connector

def connector():
    return mysql.connector.connect(
        host='localhost',  # Change this to your MySQL server host
        port=3307,
        user='raz',  # Change this to your MySQL username
        password='123456',  # Change this to your MySQL password
        database='DMD_users'  # Change this to your database name
    )

connection = connector()
cursor = connection.cursor()
