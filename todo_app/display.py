import os
import shutil
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

    def print_task_list_formatted(self, rows):
        print("Here are your current tasks:\n")

        new_rows = list(map(list, rows))
        new_rows.insert(0, ['ID', 'Added', 'Title', 'Description', 'Due', 'Finished?'])
        table_data = new_rows
        table = AsciiTable(table_data)

        # Check that the table will fit the width of the terminal
        max_width_table = sum(table.column_widths)
        term_width = shutil.get_terminal_size().columns
        if max_width_table > term_width:
            print(self.color_message('RED', f'The task list has a width of {max_width_table} and cannot fit within the terminal of width {term_width}'))
            return

        # Otherwise, the table fits and we can print it
        print(table.table)
