import sqlite3

class ExecuteQuery:
    def __init__(self, db_path, query, params=None):
        self.db_path = db_path
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        return False


if __name__ == "__main__":
    db_path = "example_users.db"

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cur.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ("Alice", 22),
            ("Bob", 27),
            ("Charlie", 35),
            ("Diana", 19)
        ])
        conn.commit()

    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)
    with ExecuteQuery(db_path, query, param) as results:
        for row in results:
            print(row)

