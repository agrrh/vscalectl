class Client(object):
    def __init__(self, api):
        self.api = api

    def do(self, args):
        print(args)
        print(self.api.cache.__dict__)
