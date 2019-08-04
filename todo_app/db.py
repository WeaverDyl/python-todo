import sqlite3
from pathlib import Path
from . import display

class DB:
    def __init__(self):
        self.db_file = Path.home() / '.todo.db'
        self.db_connection = sqlite3.connect(self.db_file)
        self.initialize_db()

        self.display = display.Display()

    def initialize_db(self):
        """ Create the database if it doesn't already exist """
        cursor = self.db_connection.cursor()

        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS task_list
                        (date TIMESTAMP DEFAULT (datetime('now', 'localtime')),
                        task text,
                        description text DEFAULT '',
                        due DATE,
                        finished BOOLEAN NOT NULL CHECK (finished in (0,1)) DEFAULT (0))
                       ''')
        self.db_connection.commit()

    def add_task(self, task, description, due, finished=0):
        """ Adds a brand new task to the database """
        cursor = self.db_connection.cursor()
        cursor.execute('INSERT INTO task_list (task, description, due, finished) VALUES (?, ?, ?, ?)', (task, description, due, finished))
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
        cursor.execute('SELECT * FROM task_list')

        initial_data = cursor.fetchall() # Returns list of rows, where each row is a tuple
        #tasks = [list(task) for task in initial_data] # converts that list of tuples to a list of lists

        tasks = []

        # Convert list of tuples to dict and add a row id to each task
        for row_id, task in enumerate(initial_data):
            new_task = {}

            new_task['ID'] = row_id
            new_task['Added'] = task[0]
            new_task['Title'] = task[1]
            new_task['Description'] = task[2]
            new_task['Due'] = task[3]
            new_task['Finished?'] = task[4]

            tasks.append(new_task)

        return tasks
