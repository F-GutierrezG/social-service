class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.admin = False if 'admin' not in data else data['admin']
        self.hash = data['hash']
