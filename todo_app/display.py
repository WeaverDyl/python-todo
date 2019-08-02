import os

class Display:
    colors = {
        'RED': '\033[38;5;196m',
        'ORANGE': '',
        'GREEN': '\033[38;5;46m',

        'BLUE': '\033[38;5;21m',
        'CYAN': '\033[38;5;51m',

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
