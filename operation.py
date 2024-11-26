from seed import create_connection, database


def get_tasks_by_user(conn, user_id):
    sql = """
    SELECT * FROM tasks WHERE user_id = ?;
    """
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    return cur.fetchall()


def get_tasks_by_status(conn, status_name):
    sql = """
    SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = ?);
    """
    cur = conn.cursor()
    cur.execute(sql, (status_name,))
    return cur.fetchall()


def update_task_status(conn, task_id, new_status_name):
    sql = """
    UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = ?) WHERE id = ?;
    """
    cur = conn.cursor()
    cur.execute(sql, (new_status_name, task_id))
    conn.commit()


def get_users_without_tasks(conn):
    sql = """
    SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def add_task_for_user(conn, title, description, status_name, user_id):
    sql = """
    INSERT INTO tasks (title, description, status_id, user_id) 
    VALUES (?, ?, (SELECT id FROM status WHERE name = ?), ?);
    """
    cur = conn.cursor()
    cur.execute(sql, (title, description, status_name, user_id))
    conn.commit()


def get_uncompleted_tasks(conn):
    sql = """
    SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def delete_task(conn, task_id):
    sql = """
    DELETE FROM tasks WHERE id = ?;
    """
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()


def find_users_by_email(conn, email_pattern):
    sql = """
    SELECT * FROM users WHERE email LIKE ?;
    """
    cur = conn.cursor()
    cur.execute(sql, (email_pattern,))
    return cur.fetchall()


def update_user_name(conn, user_id, new_name):
    sql = """
    UPDATE users SET fullname = ? WHERE id = ?;
    """
    cur = conn.cursor()
    cur.execute(sql, (new_name, user_id))
    conn.commit()


def count_tasks_by_status(conn):
    sql = """
    SELECT s.name, COUNT(t.id) 
    FROM tasks t
    JOIN status s ON t.status_id = s.id
    GROUP BY s.name;
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def get_tasks_by_user_email_domain(conn, domain):
    sql = """
    SELECT t.* 
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE ?;
    """
    cur = conn.cursor()
    cur.execute(sql, ("%" + domain,))
    return cur.fetchall()


def get_tasks_without_description(conn):
    sql = """
    SELECT * FROM tasks WHERE description IS NULL OR description = '';
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def get_users_and_tasks_in_progress(conn):
    sql = """
    SELECT u.fullname, t.title 
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    JOIN status s ON t.status_id = s.id
    WHERE s.name = 'in progress';
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def get_users_and_task_count(conn):
    sql = """
    SELECT u.fullname, COUNT(t.id) as task_count 
    FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.fullname;
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


if __name__ == "__main__":
    with create_connection(database) as conn:
        if conn is not None:
            print("Завдання користувача з user_id=1:", get_tasks_by_user(conn, 1))
            print("Завдання зі статусом 'new':", get_tasks_by_status(conn, "new"))
            update_task_status(conn, 1, "in progress")
            print("Оновив статус task_id=1 до 'in progress'.")
            print("Користувачі без завдань:", get_users_without_tasks(conn))
            add_task_for_user(
                conn, "New Task", "This is a new task description", "new", 1
            )
            print("Додаои нове завдання для користувача з user_id=1.")

            print("Незавершені завдання:", get_uncompleted_tasks(conn))
            delete_task(conn, 1)
            print("Видалено завдання task_id=1.")
            print(
                "Користувачі з поштою '@example.com':",
                find_users_by_email(conn, "%@example.com"),
            )
            update_user_name(conn, 1, "New Name")
            print("Кількість завдань за кожним статусом:", count_tasks_by_status(conn))
            print(
                "Завдання для користувачів з поштою '@example.com':",
                get_tasks_by_user_email_domain(conn, "example.com"),
            )
            print("Завдання без опису:", get_tasks_without_description(conn))
            print(
                "Користувачі та їхні завдання, які є у статусі 'in progress':",
                get_users_and_tasks_in_progress(conn),
            )
            print(
                "Користувачі та кількість їхніх завдань:",
                get_users_and_task_count(conn),
            )

        else:
            print("Error! cannot create the database connection.")
