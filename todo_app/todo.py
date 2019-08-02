import argparse, sys
from . import display

class Todo:
    def __init__(self):
        self.display = display.Display()

        self.arg_parser = self.setup_args()
        args = self.arg_parser.parse_args()

        if self.check_args(args):
            self.display.print_welcome()
            self.handle_args(self.arg_parser, args)
        else:
            self.display.print_welcome()
            self.print_tasks()

    def setup_args(self):
        """ Creates an argument parser and adds the allowed arguments """
        self.parser = argparse.ArgumentParser()
        self.group = self.parser.add_mutually_exclusive_group()

        self.group.add_argument('-a', '--add', help='Adds a new task to the task list', action='store_true')
        self.group.add_argument('-r', '--remove', help='Removes a task from the task list', action='store_true')
        self.group.add_argument('-f', '--finish', help='Sets a task to be finished', action='store_true')
        self.group.add_argument('-u', '--unfinish', help='Sets a task to be not finished', action='store_true')
        self.group.add_argument('-c', '--change', help='Updates an existing task', action='store_true')

        return self.parser

    def check_args(self, args):
        """ Returns True if an argument was given False otherwise. Used in setup """
        for arg in vars(args):
            if getattr(args, arg):
                return True
        return False

    def handle_args(self, parser, args):
        # Check the arguments and add items to the list/remove/finish tasks etc
        print(args)
        print(args.add)
        if args.add:
            pass
        if args.remove:
            pass
        if args.finish:
            pass
        if args.unfinish:
            pass
        if args.update:
            pass
        pass

    def print_tasks(self):
        rows = None # Get individual rows from task list (rows represent tasks)
        self.display.print_task_list(rows)

def run():
    Todo()
