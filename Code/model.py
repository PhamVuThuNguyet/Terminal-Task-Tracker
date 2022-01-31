import datetime


class Task:
    def __init__(self, id, task, tag, date_added=None, date_completed=None, status=None):
        self.task = task
        self.tag = tag
        self.date_added = date_added if date_added is not None else datetime.datetime.now().isoformat()
        self.date_completed = date_completed if date_completed is not None else None
        self.status = status if status is not None else 0  # 0: open, 1: completed
        self.id = id if id is not None else None
