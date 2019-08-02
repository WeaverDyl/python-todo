import sqlite3
from pathlib import Path

class DB:
    def __init__(self):
        self.path = Path.cwd()
        self.db_file = self.path / 'todo.db'
        self.db_connection = sqlite3.connect(self.db_file)
        self.initialize_db()

    def initialize_db(self):
        """ Create the database if it doesn't already exist """
        cursor = self.db_connection.cursor()

        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS task_list
                        (date TIMESTAMP DEFAULT (datetime('now', 'localtime')),
                        task text,
                        description text DEFAULT '',
                        due DATE,
                        finished BOOLEAN NOT NULL CHECK (finished in (0,1)) DEFAULT (0)
                        )''')
        self.db_connection.commit()

    def add_task(self, task, description, due, finished=0):
        """ Adds a brand new task to the database """
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO task_list (task, description, due, finished) VALUES (?, ?, ?, ?)", (task, description, due, finished))
        self.db_connection.commit()
