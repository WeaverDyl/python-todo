import os
import shutil
import timeago
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

            formatted_timestamp = timeago.format(timestamp, locale='en_short')
            formatted_finished = self.color_message('GREEN', '✓') if finished == '1' else self.color_message('RED', 'X')

            task['Added'] = formatted_timestamp
            task['Finished?'] = formatted_finished

            formatted_tasks.append(task)

        # Color as well! yellow if due date coming up, red if passed

        return formatted_tasks

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
