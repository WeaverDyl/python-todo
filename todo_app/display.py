import os
import math
import shutil
import textwrap
from datetime import datetime
from terminaltables import AsciiTable

class Display:
    def __init__(self):
        self.colors = {
            'RED': '\033[38;5;196m',
            'ORANGE': '\033[38;5;220m',
            'GREEN': '\033[38;5;46m',

            'BLUE': '\033[38;5;21m',
            'CYAN': '\033[38;5;51m',

            'BOLD': '\u001b[1m',
            'UNDERLINE': '\u001b[4m',
            'RESET': '\033[0m'
        }

        # Defines where to insert newlines in case of
        # situations where one task has some long columns
        self.max_col_widths = {
            'ID': 4,
            'Added': 10,
            'Title': 30,
            'Description': 30,
            'Due': 10,
            'Finished': 1
        }

    def color_message(self, message, *args):
        """ Sets a message to be a specific color from the colors dict before resetting """
        args_list = [str(color) for color in args]
        colors = ''.join([self.colors[i] for i in args_list])
        return ''.join([colors, message, self.colors['RESET']])

    def print_error(self, message):
        """ Prints a message in bold, red characters """
        print(self.color_message(message, 'BOLD', 'RED'))

    def print_success(self, message):
        """ Prints a message in bold, green characters """
        print(self.color_message(message, 'BOLD', 'GREEN'))

    def print_message(self, message):
        """ Prints a message in bold characters """
        print(self.color_message(message, 'BOLD'))

    @staticmethod
    def clear_terminal():
        """ Clears a terminal to prepare for output """
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_welcome(self):
        """ Prints a simple welcome message. """
        Display.clear_terminal()
        self.print_message('Welcome to python-todo!\n')

    def print_commands(self):
        """ Prints a list of available commands to run the program with.
            Shown when the user has an empty task list """
        commands = [[self.color_message(i, 'BOLD') for i in ['Commands', 'Description']],
                    ['-a/--add', 'Add a new element to a task list'],
                    ['-r/--remove', 'Remove an element from a task list'],
                    ['-f/--finish', 'Finish a task in a task list'],
                    ['-u/--unfinish', 'Unfinish a task in a task list'],
                    ['-c/--change', 'Change parts of an existing task'],
                    ['-v/--view', 'View the whole task list']]
        table_data = commands
        table = AsciiTable(table_data)
        table.inner_row_border = True

        if not self.check_table_fit(table):
            self.print_message('Try adding a task to your list! just call `python-todo -a`')
        else:
            self.print_message('Try adding a task to your list! Here\'s the available commands:')
            print(table.table)

    @staticmethod
    def check_table_fit(table):
        """ Returns true if a terminaltable will fit within the width of
            the current terminal width"""
        term_width = shutil.get_terminal_size().columns
        table_width = table.table_width
        if table_width > term_width:
            return False
        return True

    def format_row(self, tasks):
        """ Performs formatting tasks such as changing task completions from (0,1) to (X/✓) """
        formatted_tasks = []

        for task in tasks:
            # Format specific columns
            title = task['Title']
            description = task['Description']

            timestamp = task['Added']
            finished = task['Finished?']
            due = task['Due']

            formatted_timestamp = self.format_time(timestamp)
            formatted_finished = self.color_message('✓', 'GREEN', 'BOLD') if finished == 1 else self.color_message('X', 'BOLD', 'RED')
            formatted_due = self.format_due_date(due, finished)

            # Wrap long lines in the title or description
            formatted_title = self.format_long_lines(title, 'Title')
            formatted_description = self.format_long_lines(description, 'Description')

            task['Title'] = formatted_title
            task['Description'] = formatted_description
            task['Added'] = formatted_timestamp
            task['Finished?'] = formatted_finished
            task['Due'] = formatted_due

            formatted_tasks.append(task)

        return formatted_tasks

    @staticmethod
    def format_time(timestamp):
        """ Returns a nice timestamp telling the user how old a task is.
            Returns strings such as '1d ago' """
        timestamp_datetime = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        curr_time = datetime.now()
        total_time_diff = curr_time - timestamp_datetime

        # Time Constants
        SECONDS_IN_MIN = 60
        SECONDS_IN_HOUR = 3600
        SECONDS_IN_DAY = 86400
        SECONDS_IN_WEEK = 604800
        SECONDS_IN_MONTH = 2592000
        SECONDS_IN_YEAR = 31536000

        # Print out formatted time difference
        if total_time_diff.total_seconds() < 10:
            return f'just now'
        if total_time_diff.total_seconds() < SECONDS_IN_MIN:
            seconds_passed = math.floor(total_time_diff.total_seconds())
            return f'{seconds_passed}s ago'
        if total_time_diff.total_seconds() < SECONDS_IN_HOUR:
            minutes_passed = math.floor(total_time_diff.total_seconds() / SECONDS_IN_MIN)
            return f'{minutes_passed}m ago'
        if total_time_diff.total_seconds() < SECONDS_IN_DAY:
            hours_passed = math.floor(total_time_diff.total_seconds() / SECONDS_IN_HOUR)
            return f'{hours_passed}h ago'
        if total_time_diff.total_seconds() < SECONDS_IN_WEEK:
            days_passed = math.floor(total_time_diff.total_seconds() / SECONDS_IN_DAY)
            return f'{days_passed}d ago'
        if total_time_diff.total_seconds() < SECONDS_IN_MONTH:
            weeks_passed = math.floor(total_time_diff.total_seconds() / SECONDS_IN_WEEK)
            return f'{weeks_passed}w ago'
        if total_time_diff.total_seconds() < SECONDS_IN_YEAR:
            months_passed = math.floor(total_time_diff.total_seconds() / SECONDS_IN_MONTH)
            return f'{months_passed}mo ago'
        years_passed = math.floor(total_time_diff.total_seconds() / SECONDS_IN_YEAR)
        return f'{years_passed}yr ago'

    @staticmethod
    def validate_date(date_str):
        """ Ensures that the date given is in an acceptable format """
        for date_format in ('%m/%d/%Y', '%m-%d-%Y'):
            try:
                if datetime.strptime(date_str, date_format):
                    return True
            except ValueError:
                pass
        return False

    def format_due_date(self, due_date, finished):
        """ Formats the due date column to be colored based on how close
            the task is to its due date. (Red = overdue, etc...)"""
        # Don't format tasks that don't have a due date or are finished
        if due_date == '' or finished == 1:
            return due_date

        curr_time = datetime.now()

        try:
            due_date_time = datetime.strptime(due_date, '%m-%d-%Y')
        except ValueError:
            due_date_time = datetime.strptime(due_date, '%m/%d/%Y')

        time_until_due = due_date_time - curr_time

        SECONDS_IN_DAY = 86400

        # Tasks due in 24 hours or less are colored orange
        if int(time_until_due.total_seconds()) < SECONDS_IN_DAY:
            return self.color_message(due_date, 'ORANGE', 'BOLD')

        # Overdue tasks are colored red
        if int(time_until_due.total_seconds()) < 0:
            return self.color_message(due_date, 'RED', 'BOLD')

        return due_date

    def format_long_lines(self, long_text, element):
        wrapper = textwrap.TextWrapper(width=self.max_col_widths[element])
        return '\n'.join(wrapper.wrap(text=long_text))

    def print_task_list_formatted(self, rows):
        """ Prints each formatted task to the terminal in the form
            of a table """
        header = [self.color_message(i, 'BOLD') for i in ['ID', 'Added', 'Title', 'Description', 'Due', 'Finished?']]
        table_data = [task.values() for task in rows]
        table_data.insert(0, header) # The column headers are the first element of the list
        table = AsciiTable(table_data) # Create the table -- but test width before printing
        table.inner_row_border = True # Separates each task

        if not self.check_table_fit(table):
            max_width_table = table.table_width
            term_width = shutil.get_terminal_size().columns
            self.print_message(f'The task list has a width of {max_width_table} and cannot fit in the terminal of width {term_width}.')
            return

        # The table fits and we can print it
        self.print_message('Here are your current tasks:')
        print(table.table)

    # Methods for ADDING tasks
    def ask_user_title(self):
        """ Asks the user for the title of the task """
        title = ''
        while title == '':
            title = input(self.color_message('Give your task a name: ', 'BOLD'))
            if title == '':
                self.print_error('The title can\'t be an empty string!')
        return title

    def ask_user_description(self):
        """ Gets an optional description from the user """
        description = input(self.color_message('Optionally, give your task a description: ', 'BOLD'))
        return description

    def ask_user_due(self):
        """ Gets an optional due date for the task from the user """
        date = ''
        asked = False
        while not asked or not self.validate_date(date):
            date = input(self.color_message('Optionally, give your task a due date (\'mm/dd/yyyy\' or \'mm-dd-yyyy\'): ', 'BOLD'))
            asked = True
            if date == '':
                return date
            if not self.validate_date(date):
                self.print_error('That\'s not a valid date format!')
        return date

    def ask_user_finished(self):
        """ Asks a user if a task is finished """
        valid_responses = {
            'yes': True,
            'y': True,
            'no': False,
            'n': False
        }

        default_resp = False

        while True:
            user_resp = input(self.color_message('Is the task already finished? (y/N) ', 'BOLD')).lower()

            if user_resp in valid_responses:
                return valid_responses[user_resp]
            if user_resp == '':
                return default_resp
            self.print_error('That\'s not a valid answer! Answer (y/N)')

    def ask_user_id(self, action):
        """ Ask the user for a task ID to remove/finish/unfinish/update """
        row_id = input(self.color_message(f'What task would you like to {action}? (Enter an ID or `-1` to cancel): ', 'BOLD'))
        return row_id
