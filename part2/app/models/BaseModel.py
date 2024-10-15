import uuid
from datetime import datetime


class BaseModel:
    """
    A base model class that provides unique identification and timestamping for instances.

    Attributes:
        id (str): A unique identifier for the instance.
        created_at (datetime): The timestamp when the instance was created.
        updated_at (datetime): The timestamp when the instance was last updated.
    """

    def __init__(self):
        """
        Initializes a new instance of BaseModel.

        Generates a unique id using UUID and sets created_at and updated_at timestamps to the current datetime.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self) -> None:
        """
        Updates the updated_at timestamp whenever the object is modified.

        This method should be called after any changes to the object's attributes.
        """
        self.updated_at = datetime.now()

    def update(self, data: dict) -> None:
        """
        Updates the attributes of the object based on the provided dictionary.

        Args:
            data (dict): A dictionary containing attribute names and their new values.

        Updates only the attributes that exist in the object, and calls save() to update the timestamp.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def __repr__(self):
        """
        Returns a string representation of the object for debugging.

        Returns:
            str: A formatted string representing the object, including class name, id, created_at, and updated_at timestamps.
        """
        return (
            f"<{self.__class__.__name__}(id={self.id}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})>"
        )
