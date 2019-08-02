class Todo:
    def __init__(self):
        self.setup_args();
        args = self.get_args()
        self.handle_args(args)
        print("Welcome!")

    def setup_args(self):
        pass

    def get_args(self):
        pass

    def handle_args(self, args):
        pass

if __name__ == "__main__":
    Todo()
