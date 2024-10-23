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


     def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if owner is None:
            raise ValueError("Owner not found")

        place_data_copy = place_data.copy()
        amenities_ids = place_data_copy.pop('amenities', [])
        place_data_copy.pop('owner_id')
        place_data_copy['owner'] = owner

        new_place = Place(**place_data_copy)

        for amenity_id in amenities_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                new_place.add_amenity(amenity)
            else:
                raise ValueError(f"Amenity with ID '{amenity_id}' not found")

        self.place_repo.add(new_place)
        return new_place


    def get_place(self, place_id):
        """Retrieve a place by its unique ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update an existing place's information."""
        place = self.get_place(place_id)
        if place:
            for key, value in place_data.items():
                setattr(place, key, value)  # Update place attributes
            self.place_repo.update(place_id, place)
            return place
        return None

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
            return None

        if not isinstance(amenity_data, dict):
            raise ValueError("amenity_data must be a dictionary")

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
        """
        Create a new place with the provided data.

    This method creates a new place by verifying the existence of the owner,
    properly managing associated amenities, and ensuring all necessary data
    is present and valid before creating and storing the new place.

    Args:
        place_data (dict): A dictionary containing the place's attributes,
                           including 'owner_id' and optionally 'amenities'.

    Returns:
        Place: The newly created Place instance.
        """
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])

        if not user:
            raise ValueError("User not found")
        if not place:
            raise ValueError("Place not found")
        if not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5")

        new_review = Review(**review_data)
        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        """
        Retrieves a review by its ID. Returns None if not found.
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieves all reviews from the repository.
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Retrieves all reviews for a specific place by its ID.
        """
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        """
        Updates an existing review by ID. Validates new data and returns the updated review.
        """
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        if 'rating' in review_data and not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5")

        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        """
        Deletes a review by its ID.
        """
        self.review_repo.delete(review_id)


hbnb_facade = HBnBFacade()