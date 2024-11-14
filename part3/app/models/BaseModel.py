import uuid
from datetime import datetime
from app import db

class BaseModel:
    """Base class for all models in the application.

    This class provides common attributes and methods for all models, including
    unique identification (UUID), timestamps for creation and updates,
    and methods
    for converting model instances to dictionaries and updating attributes.

    Attributes:
        id (str): Unique identifier for the model instance.
        created_at (datetime): Timestamp for when the model
        instance was created.
        updated_at (datetime): Timestamp for when the model
        instance was last updated.

    Methods:
        save(): Updates the updated_at timestamp to the current time.
        to_dict(): Converts the model instance to a dictionary representation.
        update(data): Updates model attributes based on the
        provided dictionary.
    """
    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)

            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Convert the object to a dictionary"""
        result = self.__dict__.copy()
        result['__class__'] = self.__class__.__name__
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        return result

    def update(self, data):
        """Update the attributes of the object based
        on the provided dictionary"""
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at', '__class__']:
                setattr(self, key, value)
        self.save()
