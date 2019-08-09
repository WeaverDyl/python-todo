import argparse
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
            self.handle_args(args)
        else:
            # No args given. Show tasks if there are any, or commands
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

    @staticmethod
    def check_args(args):
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
            self.print_tasks()
            self.remove_task()
        if args.finish:
            self.print_tasks()
            self.finish_task()
        if args.unfinish:
            self.print_tasks()
            self.unfinish_task()
        if args.change:
            self.print_tasks()
            self.update_task()
        if args.view:
            self.view_tasks()

    def add_task(self):
        """ Adds a task to the task list """
        task_title = self.display.ask_user_title()
        task_description = self.display.ask_user_description()
        task_due = self.display.ask_user_due()

        # Call the db function to add data
        self.db_link.add_task(task_title, task_description, task_due)
        self.display.print_success('\nTask successfully added.\n')

    def remove_task(self):
        """ Removes a task from the task list """
        row_id = self.get_valid_id('remove') # Get the task ID user wants removed

        if row_id == -1:
            return

        self.db_link.remove_task(row_id) # Actually remove the task

        # If the task list is empty, print that fact, else print the rest of the tasks
        if self.db_link.get_num_tasks() > 0:
            self.display.print_success('\nTask successfully removed.\n')
            self.print_tasks()
        else:
            self.display.print_success('\nTask successfully removed. Your task list is empty.')

    def finish_task(self):
        """ Finishes a given task in the task list """
        row_id = self.get_valid_id('finish')

        if row_id == -1:
            return

        self.db_link.finish_task(row_id)
        self.display.print_success('\nTask successfully finished.\n')
        self.print_tasks()

    def unfinish_task(self):
        """" Unfinishes a given task in the task list """
        row_id = self.get_valid_id('unfinish')

        if row_id == -1:
            return

        self.db_link.unfinish_task(row_id)
        self.display.print_success('\nTask successfully unfinished.\n')
        self.print_tasks()

    def update_task(self):
        """ Updates a given task in the task list """
        row_id = self.get_valid_id('update')

        if row_id == -1:
            return

        task_title = self.display.ask_user_title()
        task_description = self.display.ask_user_description()
        task_due = self.display.ask_user_due()
        task_finished = self.display.ask_user_finished()

        # Call the db function to update data
        self.db_link.update_task(row_id, task_title, task_description, task_due, task_finished)
        self.display.print_success('\nTask successfully updated.\n')
        self.print_tasks()

    def view_tasks(self):
        """ Prints the current task list or a message if there are no tasks """
        if self.db_link.get_num_tasks() > 0:
            self.print_tasks()
        else:
            self.display.print_error('You don\'t have any tasks! Add a task by calling `python-todo -a`')

    def get_valid_id(self, action):
        """ Gets a valid row ID from the user, used for remove/finish/unfinish
            and updating rows"""
        row_id = self.display.ask_user_id(action)

        # We repeat until we get a valid ID or user cancels
        while not self.db_link.verify_id(row_id):
            # User cancelled operation
            if row_id == '-1':
                return -1

            if not self.db_link.verify_id(row_id):
                self.display.print_error('Invalid ID given')

            row_id = self.display.ask_user_id(action)

        return row_id

    def print_tasks(self):
        """ Obtains each row of the task list and prints them after formatting """
        unformatted_rows = self.db_link.get_tasks()
        formatted_rows = self.display.format_row(unformatted_rows)
        self.display.print_task_list_formatted(formatted_rows)

def run():
    """ Entry point: creates or loads a new task list if one exists """
    Todo()
