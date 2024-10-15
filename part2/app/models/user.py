# app/models/user.py

class User:
    def __init__(self, first_name, last_name, email, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
