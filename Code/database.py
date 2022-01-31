import datetime
import sqlite3

from model import Task

conn = sqlite3.connect('tasktracker.db')
cur = conn.cursor()


def create_table():
    cur.execute(
        """CREATE TABLE IF NOT EXISTS tasktracker(id integer, task text, tag text, date_added text, date_completed text, status integer)""")


create_table()


def insert(task: Task):
    cur.execute('SELECT COUNT(*) FROM tasktracker')
    count = cur.fetchone()[0]
    task.id = count if count else 0
    with conn:
        cur.execute('INSERT INTO tasktracker VALUES(:id, :task, :tag, :date_added, :date_completed, :status)',
                    {'id': task.id, 'task': task.task, 'tag': task.tag, 'date_added': task.date_added,
                     'date_completed': task.date_completed, 'status': task.status})


def select_all() -> list[Task]:
    cur.execute('SELECT * FROM tasktracker')
    res_all = cur.fetchall()
    tasks = []
    for res in res_all:
        tasks.append(Task(*res))
    return tasks


def delete(id):
    cur.execute('SELECT COUNT(*) FROM tasktracker')
    count = cur.fetchone()[0]

    with conn:
        cur.execute('DELETE FROM tasktracker WHERE id = :id', {'id': id})

    for pos in range(id + 1, count):
        update_id(pos, pos - 1, False)


def update_id(old_id: int, new_id: int, commit=True):
    with conn:
        cur.execute('UPDATE tasktracker SET id = :new_id WHERE id = :old_id',
                    {'new_id': new_id, 'old_id': old_id})
        if commit:
            conn.commit()


def update(id: int, task: str, tag: str):
    with conn:
        if task is not None and tag is not None:
            cur.execute('UPDATE tasktracker SET task = :task, tag = :tag WHERE id = :id',
                        {'task': task, 'tag': tag, 'id': id})
        elif task is not None:
            cur.execute('UPDATE tasktracker SET task = :task WHERE id = :id',
                        {'tag': tag, 'id': id})
        elif tag is not None:
            cur.execute('UPDATE tasktracker SET tag = :tag WHERE id = :id',
                        {'tag': tag, 'id': id})


def complete(id: int):
    with conn:
        cur.execute('UPDATE tasktracker SET status = "1", date_completed = :date_completed WHERE id = :id',
                    {'id': id, 'date_completed': datetime.datetime.now().isoformat()})
