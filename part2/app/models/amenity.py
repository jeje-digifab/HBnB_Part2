from app.models.BaseModel import BaseModel

class Amenity(BaseModel):
    """
    Represents an amenity in the HBnB application.

    Inherits from BaseModel, which provides common attributes:
    - id: A unique identifier for the amenity.
    - created_at: Timestamp when the amenity was created.
    - updated_at: Timestamp when the amenity was last updated.

    Attributes:
    - name (str): The name of the amenity. This is a required attribute and must not exceed 128 characters.
    - description (str): A brief description of the amenity. Optional, but must not exceed 255 characters.
    """

    def __init__(self, name: str, description: str = ""):
        """
        Initializes a new instance of the Amenity class.

        Parameters:
            name (str): The name of the amenity. This should be a non-empty string with a maximum length of 128 characters.
            description (str): A brief description of the amenity (optional). It should be a string and must not exceed 255 characters.

        Raises:
            ValueError: If the name is not provided, is not a string, or exceeds 128 characters.
                        If the description exceeds 255 characters.
        """
        super().__init__()
        
        # Validate the name attribute
        if not isinstance(name, str):
            raise ValueError("Name must be a string.")
        
        if len(name) > 128:
            raise ValueError("Name must not exceed 128 characters.")
        
        self.name = name

        # Validate the description attribute
        if len(description) > 255:
            raise ValueError("Description must not exceed 255 characters.")
        
        self.description = description

    def set_name(self, name: str):
        """
        Sets or updates the name of the amenity with validation.

        Parameters:
            name (str): The new name of the amenity. It must be a valid string not exceeding 128 characters.

        Returns:
            str: A message indicating if the name update failed due to validation errors.

        Raises:
            ValueError: If the name exceeds 128 characters or is not a string.
        """
        # Validate the new name before setting
        if not isinstance(name, str):
            return "Name must be a string."
        
        if len(name) > 128:
            return "Name must not exceed 128 characters."
        
        # Update the name and save the object to update the timestamp
        self.name = name
        self.save()

    def set_description(self, description: str):
        """
        Sets or updates the description of the amenity with validation.

        Parameters:
            description (str): The new description of the amenity. It must be a valid string not exceeding 255 characters.

        Returns:
            str: A message indicating if the description update failed due to validation errors.
        """
        # Validate the new description before setting
        if len(description) > 255:
            return "Description must not exceed 255 characters."
        
        # Update the description and save the object to update the timestamp
        self.description = description
        self.save()

    def __repr__(self):
        """
        Returns a string representation of the Amenity object for debugging and logging purposes.

        This includes the class name, unique id, name, description of the amenity, and timestamps for creation and last update.

        Returns:
            str: A formatted string representing the Amenity instance.
        """
        return (
            f"<Amenity(id={self.id}, name={self.name}, "
            f"description={self.description}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})>"
        )
