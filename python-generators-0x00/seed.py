import mysql.connector
from mysql.connector import Error
import uuid
import csv


# ------------------------------
# 1. Connect to MySQL server
# ------------------------------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password"
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f" Error: {e}")
        return None


# ------------------------------
# 2. Create database if not exists
# ------------------------------
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    print("Database ALX_prodev ready")
    cursor.close()


# ------------------------------
# 3. Connect to ALX_prodev
# ------------------------------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ALX_prodev"
        )
        if connection.is_connected():
            print("Connected to ALX_prodev")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# ------------------------------
# 4. Create user_data table
# ------------------------------
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX idx_user_id (user_id)
        )
    """)
    print("Table user_data ready")
    cursor.close()


# ------------------------------
# 5. Insert data from CSV
# ------------------------------
def insert_data(connection, data):
    cursor = connection.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM user_data WHERE email = %s", (data["email"],))
    exists = cursor.fetchone()[0]
    
    if exists == 0:
        cursor.execute(
            """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """,
            (str(uuid.uuid4()), data["name"], data["email"], data["age"])
        )
        connection.commit()
        print(f"Inserted: {data['name']}")
    else:
        print(f"Skipped (already exists): {data['email']}")
    
    cursor.close()


# ------------------------------
# 6. Seed from CSV file
# ------------------------------
def seed_from_csv(connection, csv_file="user_data.csv"):
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            insert_data(connection, row)


# ------------------------------
# MAIN EXECUTION
# ------------------------------
if __name__ == "__main__":
    # connect to server
    server_conn = connect_db()
    if server_conn:
        # create database
        create_database(server_conn)
        server_conn.close()
    
    # connect to ALX_prodev
    db_conn = connect_to_prodev()
    if db_conn:
        # create table
        create_table(db_conn)
        
        # seed data
        seed_from_csv(db_conn, "user_data.csv")
        
        db_conn.close()