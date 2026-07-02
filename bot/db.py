import os
from contextlib import contextmanager
from typing import LiteralString

from psycopg_pool import ConnectionPool

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://bot:botpass@localhost:5432/jobdb"
)
pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=5)


@contextmanager
def get_conn():
    with pool.connection() as conn:
        yield conn


def fetch_one(query: LiteralString, params: tuple = ()):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchone()


def fetch_all(query: LiteralString, params: tuple = ()):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()


def execute(query: LiteralString, params: tuple = ()):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()
