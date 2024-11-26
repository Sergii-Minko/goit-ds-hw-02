from faker import Faker
from sqlite3 import Error
import sqlite3
from contextlib import contextmanager
from functools import wraps

fake = Faker()


database = "./task.db"

seed_users = 10  # 10 користувачів
seed_tasks = 20  # 20 завдань


def manage_cursor(func):
    @wraps(func)
    def wrapper(conn, *args, **kwargs):
        cur = conn.cursor()
        try:
            result = func(cur, *args, **kwargs)
            conn.commit()
        except Error as e:
            print(e)
            result = None
        finally:
            cur.close()
        return result

    return wrapper


@contextmanager
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    yield conn
    conn.rollback()
    conn.close()


@manage_cursor
def create_user(cur, user):
    sql = """
    INSERT INTO users(fullname, email) VALUES(?,?);
    """
    cur.execute(sql, user)

    return cur.lastrowid


@manage_cursor
def create_status(cur, status):
    sql = """
    INSERT INTO status(name) VALUES(?);
    """

    cur.execute(sql, status)

    return cur.lastrowid


@manage_cursor
def create_task(cur, task):
    sql = """
    INSERT INTO tasks(title, description, status_id, user_id) VALUES(?,?,?,?);
    """
    cur.execute(sql, task)

    return cur.lastrowid


if __name__ == "__main__":
    with create_connection(database) as conn:
        if conn is not None:
            for _ in range(seed_users):
                user = (fake.name(), fake.email())
                create_user(conn, user)

            statuses = [("new",), ("in progress",), ("completed",)]
            for status in statuses:
                create_status(conn, status)

            for _ in range(seed_tasks):
                task = (
                    fake.sentence(nb_words=5),
                    fake.text(),
                    fake.random_int(min=1, max=3),
                    fake.random_int(min=1, max=seed_users),
                )
                create_task(conn, task)
        else:
            print("Error! cannot create the database connection.")
