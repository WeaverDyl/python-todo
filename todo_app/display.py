import os

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
        print("Here are your current tasks:\n\n")

        # Get extreme values for each element of the tasks (still need maximums with an option to override)
        max_len_rowid = 0
        max_len_title = 0
        max_len_desc = 0
        max_len_due = 10 # Supports up to year 9999. I'm sad to say I won't be maintaining this after that
        max_len_finished = 1 # ✓ X
        # more pythonic??
        for task in rows:
            row_id = task[0]
            title = task[2]
            description = task[3]

            if len(row_id) > max_len_rowid:
                max_len_rowid = len(row_id)
            if len(title) > max_len_title:
                max_len_title = len(title)
            if len(description) > max_len_desc:
                max_len_desc  = len(description)

        # Check if all tasks will fit into width of current window, error if not possible here
        # To get current terminal width:
        #
        # import shutil
        # shutil.get_terminal_size().columns

        for task in rows:
            row_id = task[0]
            title = task[2]
            description = task[3]
            due = task[4]
            finished = task[5]

            print(f'{row_id}\t{finished}\t{title}\t{due}\t')

