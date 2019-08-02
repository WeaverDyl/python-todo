import argparse, sys
from . import display

class Todo:
    def __init__(self):
        self.display = display.Display()

        self.arg_parser = self.setup_args()
        self.args = self.arg_parser.parse_args()

        if len(sys.argv) != 2:
            # No arguments given (argparse handles too many)
            self.display.print_welcome()
            # Print current task list
        else:
            print('Starting...')
            self.handle_args(self.args)

    def setup_args(self):
        """ Creates an argument parser and adds the allowed arguments """
        self.parser = argparse.ArgumentParser()
        self.group = self.parser.add_mutually_exclusive_group()

        self.group.add_argument('add', help='Adds a new task to the task list', nargs='?')
        self.group.add_argument('remove', help='Removes a task from the task list', nargs='?')
        self.group.add_argument('finish', help='Sets a task to be finished', nargs='?')
        self.group.add_argument('unfinish', help='Sets a task to be not finished', nargs='?')
        self.group.add_argument('update', help='Updates an existing task', nargs='?')
        self.group.add_argument('help', help='Prints a help message and quits', nargs='?')

        return self.parser

    def handle_args(self, args):
        # Check the arguments and add items to the list/remove/finish tasks etc

        pass

def run():
    Todo()
