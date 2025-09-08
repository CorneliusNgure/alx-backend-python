import mysql.connector

def paginate_users(page_size, offset):
    """Fetch one page of users starting at the given offset."""
    conn = mysql.connector.connect(
        host="localhost",
        user="kings",
        password="prenuptial",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def lazy_paginate(page_size):
    """Generator that lazily yields pages of users."""
    offset = 0
    while True: # only 1 page
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

