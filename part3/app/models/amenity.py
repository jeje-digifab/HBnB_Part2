from app.models.BaseModel import BaseModel

class Amenity(BaseModel):
    """
    Represents an amenity in the HBnB application.

    Inherits from BaseModel, which provides common attributes:
    - id: A unique identifier for the amenity.
    - created_at: Timestamp when the amenity was created.
    - updated_at: Timestamp when the amenity was last updated.

    Attributes:
    - name (str): The name of the amenity. This is a required attribute and
    must not exceed 50 characters.
    - description (str): A brief description of the amenity.
    Optional, but must not exceed 255 characters.
    """

    def __init__(self, name: str, description: str = None):
        """
        Initializes a new instance of the Amenity class.
        """
        super().__init__()
        self.set_name(name)
        self.description = description  # Optional attribute


    def set_name(self, name: str):
        """
        Sets or updates the name of the amenity with validation.
        """
        # Validate the new name before setting
        if not isinstance(name, str):
            raise ValueError("Name must be a string.")
        if not name:
            raise ValueError("Name must not be empty.")
        if len(name) > 50:
            raise ValueError("Name must not exceed 50 characters.")

        # Update the name and save the object to update the timestamp
        self.name = name
        self.save()

    def __repr__(self):
        """
        Returns a string representation of the Amenity object for
        debugging and logging purposes.
        """
        return (
            f"<Amenity(id={self.id}, name={self.name}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})>"
        )