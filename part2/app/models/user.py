from app.models import BaseModel
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re


class User(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email = self.validate_email(kwargs.get('email'))
        self.set_password(kwargs.get('password'))
        self.first_name = self.validate_first_name(
            kwargs.get('first_name', ''), "First Name")
        self.last_name = self.validate_last_name(
            kwargs.get('last_name', ''), "Last Name")
        self.is_admin = kwargs.get('is_admin', False)
        self.is_owner = kwargs.get('is_owner', False)
        self.owned_places = []
        self.rented_places = []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __str__(self):
        return "User: {}".format(self.email)

    def become_owner(self):
        """a user becomes an owner"""
        self.is_owner = True

    def add_owned_place(self, place):
        """add a place to the user's owned places"""
        if self.is_owner:
            self.owned_places.append(place)
        else:
            raise ValueError("User must be an owner to add owned places")

    def rent_place(self, place):
        """add a place to the user's rented places"""
        self.rented_places.append(place)

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
            "is_owner": self.is_owner,
            "owned_places": [place.id for place in self.owned_places],
            "rented_places": [place.id for place in self.rented_places],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()})

        user_dict.pop("password", None)
        return user_dict

    @staticmethod
    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email

    @staticmethod
    def validate_name(name, field_name):
        if len(name) > 50:
            raise ValueError(f"{field_name} must be less than 50 characters")
        return name

    def save(self):
        self.updated_at = datetime.utcnow()
        super().save()

    def update(self, data):
        if 'email' in data:
            data['email'] = self.validate_email(data['email'])
        if 'first_name' in data:
            data['first_name'] = self.validate_name(
                data['first_name'], "First Name")
        if 'last_name' in data:
            data['last_name'] = self.validate_name(
                data['last_name'], "Last Name")
        if 'password' in data:
            self.set_password(data['password'])
            data.pop('password', None)

        super().update(data)

    def set_password(self, password):
        if password:
            self.password = generate_password_hash(password)
        else:
            raise ValueError("Password is required")

    def check_password(self, password):
        return check_password_hash(self.password, password)
