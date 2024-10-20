from app.models.BaseModel import BaseModel
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re


class User(BaseModel):
    """Represents a user in the application.

    Inherits from BaseModel and includes attributes for user identification,
    authentication, and management of owned and rented places.
    """

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
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

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

    def save(self):
        """Update the updated_at timestamp and save the user instance."""
        self.updated_at = datetime.utcnow()
        super().save()

    def update(self, data):
        """Update user attributes with provided data.

        Args:
            data (dict): A dictionary of attributes to update.
        """
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
        """Set the user's password after hashing it.

        Args:
            password (str): The password to set.

        Raises:
            ValueError: If no password is provided.
        """
        if password:
            self.password = generate_password_hash(password)
        else:
            raise ValueError("Password is required")

    def check_password(self, password):
        """Check if the provided password matches the user's hashed password.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password)
