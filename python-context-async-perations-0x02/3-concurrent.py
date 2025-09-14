import asyncio
import aiosqlite

DB_PATH = "async_users.db"


async def setup_db():
    """Demo users table with some sample data."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DROP TABLE IF EXISTS users")
        await db.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        """)
        await db.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [
                ("Alice", 22),
                ("Bob", 45),
                ("Charlie", 35),
                ("Diana", 52),
                ("Eve", 41),
            ]
        )
        await db.commit()


async def async_fetch_users():
    """Fetch all users from the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows


async def async_fetch_older_users():
    """Fetch users older than 40 from the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            return rows


async def fetch_concurrently():
    """Run both fetches concurrently and print results."""
    # Run both coroutines at the same time
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("=== All Users ===")
    for row in all_users:
        print(row)

    print("\n=== Users older than 40 ===")
    for row in older_users:
        print(row)


if __name__ == "__main__":
    asyncio.run(setup_db())
    asyncio.run(fetch_concurrently())

