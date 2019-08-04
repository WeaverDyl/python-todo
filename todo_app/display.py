import os
import math
import shutil
from datetime import datetime
from terminaltables import AsciiTable
from . import db

class Display:
    colors = {
        'RED': '\033[38;5;196m',
        'ORANGE': '\033[38;5;214',
        'GREEN': '\033[38;5;46m',

        'BLUE': '\033[38;5;21m',
        'CYAN': '\033[38;5;51m',

        'BOLD': '\u001b[1m',
        'UNDERLINE': '\u001b[4m',
        'RESET': '\033[0m'
    }

    def color_message(self, message, *args):
        """ Sets a message to be a specific color from the colors dict before resetting """
        args_list = [str(color) for color in args]
        return ''.join([''.join([self.colors[i] for i in args_list]), message, self.colors['RESET']])

    @staticmethod
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_welcome(self):
        """ Prints a simple welcome message. """
        Display.clear_terminal()
        print(self.color_message('Welcome to python-todo!\n', 'BOLD'))

    def print_commands(self):
        """ Prints a list of available commands to run the program with.
            Shown when the user has an empty task list """
        pass

    def format_row(self, tasks):
        """ Performs formatting tasks such as changing task completions from (0,1) to (X/✓) """
        formatted_tasks = []

        for task in tasks:
            # Format specific columns
            timestamp = task['Added']
            finished = task['Finished?']

            formatted_timestamp = self.format_time(timestamp)
            formatted_finished = self.color_message('✓', 'GREEN') if finished == '1' else self.color_message('X', 'RED')

            task['Added'] = formatted_timestamp
            task['Finished?'] = formatted_finished

            formatted_tasks.append(task)

        # Color as well! yellow if due date coming up, red if passed

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

    def print_task_list_formatted(self, rows):
        """ Formats the rows to a table that's printed to the terminal.
            The rows are a list of dictionaries containing info for each
            row. """
        header = [self.color_message(i, 'BOLD') for i in ['ID', 'Added', 'Title', 'Description', 'Due', 'Finished?']]
        table_data = [task.values() for task in rows]
        table_data.insert(0, header) # The column headers are the first element of the list
        table = AsciiTable(table_data) # Create the table -- but test width before printing

        # Check that the table will fit the width of the terminal
        max_width_table = sum(table.column_widths)
        term_width = shutil.get_terminal_size().columns
        if max_width_table > term_width:
            print(self.color_message(f'The task list has a width of {max_width_table} and cannot fit within the terminal of width {term_width}', 'RED', 'BOLD'))
            return

        # The table fits and we can print it
        print(self.color_message('Here are your current tasks:\n', 'BOLD'))
        print(table.table)


    # Methods for ADDING tasks
    def ask_user_title(self):
        """ Asks the user for the title of the task """
        title = ''
        while title == '':
            title = input(self.color_message('Give your task a name: ', 'BOLD'))
            if title == '':
                print(self.color_message('The title can\'t be an empty string!', 'BOLD'))
        return title

    def ask_user_description(self):
        """ Gets an optional description from the user """
        description = input(self.color_message('Optionally, give your task a description: ', 'BOLD'))
        return description

    def ask_user_due(self):
        """ Gets an optional due date for the task from the user """
        date = ''
        asked = False
        while asked == False or not self.validate_date(date):
            # RED
            date = input(self.color_message('Optionally, give your task a due date (\'mm/dd/yyyy or mm-dd-yyyy\'): ', 'BOLD'))
            asked = True
            if date == '':
                return date
            if not self.validate_date(date):
                print(self.color_message('That\'s not a valid date format!', 'RED', 'BOLD'))
        return date

    def validate_date(self, date_str):
        """ Ensures that the date given is in an acceptable format """
        for date_format in ('%m/%d/%Y', '%m-%d-%Y'):
            try:
                if datetime.strptime(date_str, date_format):
                    return True
            except ValueError:
                pass
        return False

