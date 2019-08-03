import argparse
import datetime
from . import display
from . import db

class Todo:
    def __init__(self):
        self.display = display.Display()
        self.db_link = db.DB()

        self.arg_parser = self.setup_args()
        args = self.arg_parser.parse_args()

        if self.check_args(args):
            self.display.print_welcome()
            self.handle_args(args)
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
        task_title = self.ask_user_title()
        task_description = self.ask_user_description()
        task_due = self.ask_user_due()

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

    def ask_user_title(self):
        """ Asks the user for the title of the task """
        title = ''
        while title == '':
            title = input('Give your task a name: ')
            if title == '':
                print('The title can\'t be an empty string!')
        return title

    def ask_user_description(self):
        """ Gets an optional description from the user """
        description = input('Optionally, give your task a description: ')
        return description

    def ask_user_due(self):
        """ Gets an optional due date for the task from the user """
        date = ''
        asked = False
        while asked == False or not self.validate_date(date):
            date = input('Optionally, give your task a due date (\'mm/dd/yyyy or mm-dd-yyyy\') ')
            asked = True
            if date == '':
                return date
            if not self.validate_date(date):
                print('That\'s not a valid date format!')
        return date

    def validate_date(self, date_str):
        """ Ensures that the date given is in an acceptable format """
        for date_format in ('%m/%d/%Y', '%m-%d-%Y'):
            try:
                if datetime.datetime.strptime(date_str, date_format):
                    return True
            except ValueError:
                pass
        return False

    def print_tasks(self):
        unformatted_rows = self.db_link.get_tasks()
        formatted_rows = self.display.format_row(unformatted_rows)
        self.display.print_task_list_formatted(formatted_rows)

def run():
    """ Entry point: creates or loads a new task list if one exists """
    Todo()

