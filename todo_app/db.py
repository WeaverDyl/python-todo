import sqlite3
from pathlib import Path

class DB:
    def __init__(self):
        self.db_file = Path.home() / '.todo.db'
        self.db_connection = sqlite3.connect(self.db_file)
        self.initialize_db()

    def initialize_db(self):
        """ Create the database if it doesn't already exist """
        cursor = self.db_connection.cursor()

        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS task_list
                        (date TIMESTAMP DEFAULT (datetime('now', 'localtime')),
                        title text,
                        description text DEFAULT '',
                        due DATE,
                        finished BOOLEAN NOT NULL CHECK (finished in (0,1)) DEFAULT (0))
                       ''')
        self.db_connection.commit()

    def add_task(self, title, description, due, finished=0):
        """ Adds a brand new task to the database """
        cursor = self.db_connection.cursor()
        cursor.execute('INSERT INTO task_list (title, description, due, finished) VALUES (?, ?, ?, ?)', (title, description, due, finished))
        self.db_connection.commit()

    def remove_task(self, row_id):
        """ Removes a task from the task list given its ID """
        cursor = self.db_connection.cursor()
        cursor.execute('DELETE FROM task_list WHERE ROWID = (?)', (row_id,))
        self.db_connection.commit()
        cursor.execute('VACUUM') # Clean up ID's

    def finish_task(self, row_id):
        """ Changes a task from being unfinished to finished """
        cursor = self.db_connection.cursor()
        cursor.execute('UPDATE task_list SET finished = 1 WHERE ROWID = (?)', (row_id,))
        self.db_connection.commit()

    def unfinish_task(self, row_id):
        """ Changes a task from being finished to unfinished """
        cursor = self.db_connection.cursor()
        cursor.execute('UPDATE task_list SET finished = 0 WHERE ROWID = (?)', (row_id,))
        self.db_connection.commit()

    def update_task(self, row_id, title, description, due, finished):
        """ Updates an existing task in the task list """
        cursor = self.db_connection.cursor()
        cursor.execute('''UPDATE task_list SET
                            title = ?,
                            description = ?,
                            due = ?,
                            finished = ?
                          WHERE ROWID = ?''', (title, description, due, finished, row_id,))
        self.db_connection.commit()

    def get_num_tasks(self):
        """ Returns the number of tasks in the task list """
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM task_list')
        num = cursor.fetchone()

        return num[0]

    def get_tasks(self):
        """ Returns a list of each row in the database (corresponds to tasks) """
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT ROWID, * FROM task_list')

        initial_data = cursor.fetchall() # Returns list of rows, where each row is a tuple

        # Convert list of tuples to dict and add a row id to each task
        tasks = []
        for task in initial_data:
            new_task = {}

            new_task['ID'] = task[0]
            new_task['Added'] = task[1]
            new_task['Title'] = task[2]
            new_task['Description'] = task[3]
            new_task['Due'] = task[4]
            new_task['Finished?'] = task[5]

            tasks.append(new_task)

        return tasks

    def verify_id(self, row_id):
        """ Returns true if there is a row in the database that matches
            the task ID the user gave, False otherwise """
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM task_list where ROWID=(?)', (row_id,))
        num_count = cursor.fetchone()

        # If there are no matching ID's, it must not be a valid task ID
        if num_count[0] == 0:
            return False
        return True
