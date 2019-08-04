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
            self.finish_task()
            self.print_tasks()
        if args.unfinish:
            self.unfinish_task()
            self.print_tasks()
        if args.change:
            self.update_task()
            self.print_tasks()
        if args.view:
            self.print_tasks()

    def add_task(self):
        """ Adds a task to the task list """
        task_title = self.display.ask_user_title()
        task_description = self.display.ask_user_description()
        task_due = self.display.ask_user_due()

        # Call the db function to add data
        self.db_link.add_task(task_title, task_description, task_due)
    def remove_task(self):
        """ Removes a task from the task list """
        row_id = self.display.ask_user_id('remove') # Get the task ID user wants removed

        # Check that the ID is valid
        if not self.db_link.verify_id(row_id):
            print(self.display.color_message('Invalid ID given!', 'BOLD', 'RED'))
            self.remove_task() # recall until user quits or gives valid ID
        else:
            self.db_link.remove_task(row_id)

            if self.db_link.get_num_tasks() > 0:
                print(self.display.color_message('Task successfully removed.', 'BOLD'))
                self.print_tasks()
            else:
                print(self.display.color_message('Task successfully removed. Your task list is empty', 'BOLD'))
    def finish_task(self):
        """ Finishes a given task in the task list """
        # show task list and ask for id to finish
        pass
    def unfinish_task(self):
        """ Unfinishes a given task in the task list """
        # show task list and ask for id to unfinish
        pass
    def update_task(self):
        """ Updates a given task in the task list """
        # show task list and ask for id to update
        # then ask what to update (title/description/due date/finished)
        pass

    def print_tasks(self):
        """ Obtains each row of the task list and prints them after formatting """
        unformatted_rows = self.db_link.get_tasks()
        formatted_rows = self.display.format_row(unformatted_rows)
        self.display.print_task_list_formatted(formatted_rows)

def run():
    """ Entry point: creates or loads a new task list if one exists """
    Todo()
