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
        """Create a review instance from the provided data."""
        try:
            print(f"Creating review with data: {review_data}")  # Log the input data

            # Fetch the place and user by ID
            place = self.place_repo.get(review_data['place_id'])
            user = self.user_repo.get(review_data['user_id'])

            review = Review(
                text=review_data['text'],
                rating=review_data['rating'],
                place=place,
                user=user
            )
            self.review_repo.add(review)
            return review
        except KeyError as e:
            raise ValueError(f"Missing required field: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error while creating review: {str(e)}")

    def get_review(self, review_id):
        """Retrieve a review by its unique ID.

        Args:
            review_id (str): The unique identifier of the review.

        Returns:
            Review: The Review instance if found, otherwise None.
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews in the repository.

        Returns:
            list: A list of Review instances.
        """
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """Update an existing review with new data.

        Args:
            review_id (str): The unique identifier of the review to update.
            review_data (dict): A dictionary containing the updated review attributes.

        Returns:
            Review: The updated Review instance if the review was found and updated,
            otherwise None.
        """
        review = self.get_review(review_id)
        if review:
            for key, value in review_data.items():
                setattr(review, key, value)
            self.review_repo.update(review_id, review)
            return review
        return None

    def delete_review(self, review_id):
        """Delete a review by its unique ID.

        Args:
            review_id (str): The unique identifier of the review.

        Returns:
            bool: True if the review was successfully deleted, otherwise False.
        """
        return self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id):
        """Get all reviews associated with a specific place.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            list: A list of Review instances associated with the place.
        """
        return [review for review in self.review_repo.get_all() if review.place.id == place_id]


hbnb_facade = HBnBFacade()