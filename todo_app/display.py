import os
import math
import shutil
from datetime import datetime, timedelta
from terminaltables import AsciiTable

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

    def color_message(self, color, message):
        """ Sets a message to be a specific color from the colors dict before resetting """
        return ''.join([self.colors[color], message, self.colors['RESET']])

    @staticmethod
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_welcome(self):
        """ Prints a simple welcome message. """
        Display.clear_terminal()
        print('Welcome to python-todo!')

    def format_row(self, tasks):
        formatted_tasks = []

        for task in tasks:
            # Format specific columns
            timestamp = task['Added']
            finished = task['Finished?']

            formatted_timestamp = self.format_time(timestamp)
            formatted_finished = self.color_message('GREEN', '✓') if finished == '1' else self.color_message('RED', 'X')

            task['Added'] = formatted_timestamp
            task['Finished?'] = formatted_finished

            formatted_tasks.append(task)

        # Color as well! yellow if due date coming up, red if passed

        return formatted_tasks

    def format_time(self, timestamp):
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
        header = [self.color_message('BOLD', i) for i in ['ID', 'Added', 'Title', 'Description', 'Due', 'Finished?']]
        table_data = [task.values() for task in rows]
        table_data.insert(0, header) # The column headers are the first element of the list
        table = AsciiTable(table_data) # Create the table -- but test width before printing

        # Check that the table will fit the width of the terminal
        max_width_table = sum(table.column_widths)
        term_width = shutil.get_terminal_size().columns
        if max_width_table > term_width:
            print(self.color_message('RED', f'The task list has a width of {max_width_table} and cannot fit within the terminal of width {term_width}'))
            return

        # The table fits and we can print it
        print("Here are your current tasks:\n")
        print(table.table)
