from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    """Facade for managing users and places in the HBnB application.

    This class provides an interface to interact with user and place
    repositories, allowing for operations such as creating, retrieving,
    updating, and authenticating users.
    """

    def __init__(self):
        """Initialize the HBnBFacade with in-memory repositories for users,
        places, reviews, and amenities.
        """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user with the provided data.

        Args:
            user_data (dict): A dictionary containing user attributes.

        Returns:
            User: The created User instance.
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by their unique ID.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            User: The User instance if found, otherwise None.
        """
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Retrieve all users in the repository.

        Returns:
            list: A list of User instances.
        """
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """Retrieve a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            User: The User instance if found, otherwise None.
        """
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update an existing user with new data.

        Args:
            user_id (str): The unique identifier of the user to update.
            user_data (dict): A dictionary containing the
            updated user attributes.

        Returns:
            User: The updated User instance if the user was found and updated,
            otherwise None.
        """
        user = self.get_user(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.user_repo.update(user_id, user_data)
            return user
        return None

    def authenticate_user(self, email, password):
        """Authenticate a user by checking their email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password provided for authentication.

        Returns:
            User: The authenticated User instance
            if successful, otherwise None.
        """
        user = self.user_repo.get_by_attribute('email', email)
        if user and user.check_password(password):
            return user
        return None

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):

        # Logic will be implemented in later tasks
        pass

    def create_amenity(self, amenity_data):
        """Create a new amenity with the provided data."""
        if not isinstance(amenity_data, dict):
            raise ValueError("amenity_data must be a dictionary")

        name = amenity_data.get("name")
        description = amenity_data.get("description", None)  # Optional

        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity


    def get_amenity(self, amenity_id):
        """Retrieve an amenity by its unique ID.

        Args:
            amenity_id (str): The unique identifier of the amenity.

        Returns:
            Amenity: The Amenity instance if found, otherwise None.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities in the repository.
        Returns:
            list: A list of Amenity instances.
        """
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        """
        Args:
            amenity_id (str): The unique identifier of the amenity to update.
            amenity_data (dict): A dictionary containing the attributes to update.
        Returns:
            Amenity: The updated Amenity instance if the amenity was found and updated,
                    otherwise None.
        Raises:
            ValueError: If the provided amenity_data is not a dictionary or if it
                        contains invalid fields.
        """
        amenity = self.amenity_repo.get(amenity_id)

        if not amenity:
            return None  # Return None if the amenity with the given ID was not found

        if not isinstance(amenity_data, dict):
            raise ValueError("amenity_data must be a dictionary")

        # Update the amenity's attributes based on the provided data
        for key, value in amenity_data.items():
            if hasattr(amenity, key):
                setattr(amenity, key, value)  # Update the attribute with the new value
            else:
                raise ValueError(f"Invalid attribute '{key}' for Amenity")
        return amenity


    def delete_amenity(self, amenity_id):
        """Delete an amenity by its ID.
        Args:
            amenity_id (str): The unique identifier of the amenity to delete.
        Returns:
            bool: True if the amenity was successfully deleted, otherwise False.
        """
        return self.amenity_repo.delete(amenity_id)


    def create_review(self, review_data):
        # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        pass

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        pass

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        pass

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        pass

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        pass