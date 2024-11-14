from app import db
from app.models.BaseModel import BaseModel
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
import re


class User(BaseModel, db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_owner = db.Column(db.Boolean, default=False)

    owned_places = db.relationship('Place', backref='owner', lazy=True)
    rented_places = db.relationship('Place', backref='renter', lazy=True)

    def __init__(self, **kwargs):
        """Initialize a User instance with given attributes.

        Args:
            **kwargs: Keyword arguments for user attributes, including email,
                password, first_name, last_name, is_admin, and is_owner.
        """
        super().__init__(**kwargs)

        self.email = self.validate_email(kwargs.get('email'))
        self.set_password(kwargs.get('password'))
        self.first_name = self.validate_name(
            kwargs.get('first_name', ''), "First Name")
        self.last_name = self.validate_name(
            kwargs.get('last_name', ''), "Last Name")
        self.is_admin = kwargs.get('is_admin', False)
        self.is_owner = kwargs.get('is_owner', False)
        self.owned_places = []
        self.rented_places = []

    def __str__(self):
        """Return a string representation of the User instance."""
        return "User: {}".format(self.email)

    def become_owner(self):
        """Mark the user as an owner."""
        self.is_owner = True

    def add_owned_place(self, place):
        """Add a place to the user's list of owned places.

        Args:
            place: The place to be added.

        Raises:
            ValueError: If the user is not an owner.
        """
        if self.is_owner:
            self.owned_places.append(place)
        else:
            raise ValueError("User must be an owner to add owned places")

    def rent_place(self, place):
        """Add a place to the user's list of rented places.

        Args:
            place: The place to be added.
        """
        self.rented_places.append(place)

    def to_dict(self):
        """Convert the User instance to a dictionary.

        Returns:
            dict: A dictionary representation of the user,
            excluding the password.
        """
        user_dict = {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
            "is_owner": self.is_owner,
            "owned_places": [place.id for place in self.owned_places],
            "rented_places": [place.id for place in self.rented_places],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        return user_dict

    @staticmethod
    def validate_email(email):
        """Validate the provided email address.

        Args:
            email (str): The email address to validate.

        Raises:
            ValueError: If the email address is invalid.

        Returns:
            str: The validated email address.
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email

    @staticmethod
    def validate_name(name, field_name):
        """Validate the provided name.

        Args:
            name (str): The name to validate.
            field_name (str): The name of the field being
            validated (e.g., "First Name").

        Raises:
            ValueError: If the name is empty or exceeds 50 characters.

        Returns:
            str: The validated name.
        """
        if not name or len(name) > 50:
            raise ValueError(f"{field_name} must be less than 50 characters")
        return name

    def set_password(self, password):
        """Set the user's password after hashing it."""
        if password:
            self.password = generate_password_hash(password).decode('utf-8')
        else:
            raise ValueError("Password is required")

    def check_password(self, password):
        """Check if the provided password matches the user's hashed password"""
        return check_password_hash(self.password, password)
