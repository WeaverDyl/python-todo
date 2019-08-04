import argparse
import datetime
from . import display
from . import db

class Todo:
    def __init__(self):
        self.display = display.Display()
        self.db_link = db.DB()

        # Set up arguments
        self.arg_parser = self.setup_args()
        args = self.arg_parser.parse_args()

        # Always print a welcome
        self.display.print_welcome()

        # Check for arguments
        if self.check_args(args):
            # Program was passed arguments
            self.handle_args(args)
        else:
            # Program was run simply as 'python-todo'. Instead of showing an
            # empty task list (if there are no tasks), show the commands that
            # can be used instead.
            if self.db_link.get_num_tasks() == 0:
                self.display.print_commands()
            else:
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
        self.group.add_argument('-v', '--view', help='View your current task list', action='store_true')

        return self.parser

    def check_args(self, args):
        """ Returns True if an argument was given False otherwise. Used in setup """
        for arg in vars(args):
            if getattr(args, arg):
                return True
        return False

    def handle_args(self, args):
        """ Handler for each valid argument """
        if args.add:
            self.add_task()
            self.print_tasks()
        if args.remove:
            self.remove_task()
        if args.finish:
            self.finish_task()
        if args.unfinish:
            self.unfinish_task()
        if args.change:
            self.update_task()
        if args.view:
            self.print_tasks()

    def add_task(self):
        task_title = self.display.ask_user_title()
        task_description = self.display.ask_user_description()
        task_due = self.display.ask_user_due()

        self.db_link.add_task(task_title, task_description, task_due) # Call the db function to add data
    def remove_task(self):
        # show task list and ask for id to remove
        pass
    def finish_task(self):
        # show task list and ask for id to finish
        pass
    def unfinish_task(self):
        # show task list and ask for id to unfinish
        pass
    def update_task(self):
       # show task list and ask for id to update
       # then ask what to update (title/description/due date/finished)
       pass

    def print_tasks(self):
        unformatted_rows = self.db_link.get_tasks()
        formatted_rows = self.display.format_row(unformatted_rows)
        self.display.print_task_list_formatted(formatted_rows)

def run():
    """ Entry point: creates or loads a new task list if one exists """
    Todo()

