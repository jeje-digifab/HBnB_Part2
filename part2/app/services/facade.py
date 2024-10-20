from app.persistence.repository import InMemoryRepository
from app.models.user import User


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
