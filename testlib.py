class FakeLogger:
    def __init__(self):
        self.logged = False
        self.logged_list = []
        self.contents = ''

    def log(self, x, y):
        self.logged = True
        self.contents += '{} {}'.format(x, y)

    def log_to_list(self, x, y):
        self.logged_list.append(True)
        self.contents += '{} {}'.format(x, y)

    def reset(self):
        self.logged = False
        self.logged_list = []
        self.contents = ''
