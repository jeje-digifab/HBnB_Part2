import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self) -> None:
        """
        Update the updated_at timestamp whenever the object is modified
        """
        self.updated_at = datetime.now()

    def update(self, data: dict) -> None:
        """
        Update the attributes of the object based on the provided dictionary
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})>"
