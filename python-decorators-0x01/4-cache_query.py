import time
import sqlite3 
import functools


query_cache = {}

#### with_db_connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


#### cache_query decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if query is passed via kwargs or args
        query = kwargs.get("query")
        if query is None and len(args) > 1:  
            # args[0] = conn, args[1] = query
            query = args[1]

        if query in query_cache:
            print(f"[CACHE HIT] Returning cached results for: {query}")
            return query_cache[query]

        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"[CACHE MISS] Executed and cached results for: {query}")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
