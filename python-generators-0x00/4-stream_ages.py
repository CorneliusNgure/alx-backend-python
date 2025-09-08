import mysql.connector

def stream_user_ages():
    """Generator that yields user ages one by one from the database."""
    conn = mysql.connector.connect(
        host="localhost",
        user="kings",
        password="prenuptial",
        database="ALX_prodev"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # cursor itself is iterable
        yield int(age)     # yield one age at a time

    cursor.close()
    conn.close()


def calculate_average_age():
    """Calculate average age using the generator, memory-efficiently."""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")
