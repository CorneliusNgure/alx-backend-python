import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields rows from user_data in batches."""
    conn = mysql.connector.connect(
        host="localhost",
        user="kings",
        password="prenuptial",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)  # dictionary=True → returns dict rows

    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """Generator that processes batches and yields users over age 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if int(user["age"]) > 25:
                yield user
