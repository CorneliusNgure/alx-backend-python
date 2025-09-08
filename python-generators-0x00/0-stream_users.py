#!/usr/bin/python3
import mysql.connector

def stream_users():
    """Generator that streams rows from user_data table one by one"""
    conn = mysql.connector.connect(
        host="localhost",
        user="kings",
        password="prenuptial",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row

    cursor.close()
    conn.close()

