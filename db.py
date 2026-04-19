import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="super123",   # <-- change this
        database="civic_system"
    )
