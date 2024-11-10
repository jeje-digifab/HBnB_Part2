from app.persistence.repository import SQLAlchemyRepository
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
        """
        Initialize the HBnBFacade with in-memory repositories.
        Switched to SQLAlchemyRepository
        """


        self.user_repository = SQLAlchemyRepository(User)
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        """Create a new user with the provided data."""
        user = User(**user_data)
        self.user_repository.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by their unique ID."""
        return self.user_repository.get(user_id)

    def get_all_users(self):
        """Retrieve all users in the repository."""
        return self.user_repository.get_all()

    def get_user_by_email(self, email):
        """Retrieve a user by their email address."""
        return self.user_repository.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update an existing user with new data."""
        user = self.get_user(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.user_repository.update(user_id, user_data)
            return user
        return None

    def authenticate_user(self, email, password):
        """Authenticate a user by checking their email and password."""
        user = self.user_repository.get_by_attribute('email', email)
        if user and user.check_password(password):
            return user
        return None

    def create_place(self, place_data):
        """Create a new place associated with an owner and amenities."""
        owner_id = place_data.get('owner_id')
        owner = self.user_repository.get(owner_id)
        if owner is None:
            raise ValueError("Owner not found")

        place_data_copy = place_data.copy()
        amenities_ids = place_data_copy.pop('amenities', [])
        place_data_copy.pop('owner_id')
        place_data_copy['owner'] = owner

        new_place = Place(**place_data_copy)
        for amenity_id in amenities_ids:
            amenity = self.amenity_repository.get(amenity_id)
            if amenity:
                new_place.add_amenity(amenity)
            else:
                raise ValueError(f"Amenity with ID '{amenity_id}' not found")

        self.place_repository.add(new_place)
        return new_place

    def get_place(self, place_id):
        """Retrieve a place by its unique ID."""
        return self.place_repository.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        """Update an existing place's information."""
        place = self.get_place(place_id)
        if place:
            if not isinstance(place_data, dict):
                raise ValueError("place_data must be a dictionary")

            for key, value in place_data.items():
                if key in ['title', 'description', 'price', 'latitude', 'longitude']:
                    setattr(place, key, value)
                elif key == 'owner_id':
                    owner = self.user_repository.get(value)
                    if owner:
                        place.owner = owner
                    else:
                        raise ValueError(f"Owner with ID '{value}' not found")
                else:
                    raise ValueError(f"Invalid attribute '{key}' for Place")
            self.place_repository.update(place_id, place_data)
            return place
        return None

    def create_amenity(self, amenity_data):
        """Create a new amenity with the provided data."""
        if not isinstance(amenity_data, dict):
            raise ValueError("amenity_data must be a dictionary")

        name = amenity_data.get("name")
        description = amenity_data.get("description", None)

        amenity = Amenity(**amenity_data)
        self.amenity_repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by its unique ID.

        Args:
            amenity_id (str): The unique identifier of the amenity.

        Returns:
            Amenity: The Amenity instance if found, otherwise None.
        """
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities in the repository.
        Returns:
            list: A list of Amenity instances.
        """
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Args:
            amenity_id (str): The unique identifier of the amenity to update.
            amenity_data (dict): A dictionary containing the
                attributes to update.
        Returns:
            Amenity: The updated Amenity instance if the amenity
                was found and updated,
                    otherwise None.
        Raises:
            ValueError: If the provided amenity_data is
                not a dictionary or if it
                        contains invalid fields.
        """
        amenity = self.amenity_repository.get(amenity_id)

        if not amenity:
            return None

        if not isinstance(amenity_data, dict):
            raise ValueError("amenity_data must be a dictionary")

        for key, value in amenity_data.items():
            if hasattr(amenity, key):
                # Update the attribute with the new value
                setattr(amenity, key, value)
            else:
                raise ValueError(f"Invalid attribute '{key}' for Amenity")
        return amenity

    def delete_amenity(self, amenity_id):
        """Delete an amenity by its ID.
        Args:
            amenity_id (str): The unique identifier of the amenity to delete.
        Returns:
            bool: True if the amenity was successfully deleted,
                otherwise False.
        """
        return self.amenity_repository.delete(amenity_id)

    def create_review(self, review_data):
        """Create a review instance from the provided data."""
        try:
            print(f"Creating review with data: {review_data}")
            place = self.place_repository.get(review_data['place_id'])
            user = self.user_repository.get(review_data['user_id'])

            review = Review(
                text=review_data['text'],
                rating=review_data['rating'],
                place=place,
                user=user
            )
            self.review_repository.add(review)
            return review
        except KeyError as e:
            raise ValueError(f"Missing required field: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error while creating review: {str(e)}")

    def get_review(self, review_id):
        """Retrieve a review by its unique ID."""
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews in the repository."""
        return self.review_repository.get_all()

    def update_review(self, review_id, review_data):
        """Update an existing review with new data."""
        review = self.get_review(review_id)
        if review:
            if not isinstance(review_data, dict):
                raise ValueError("review_data must be a dictionary")

            for key, value in review_data.items():
                if key in ['text', 'rating']:
                    setattr(review, key, value)
                elif key == 'user_id':
                    user = self.user_repository.get(value)
                    if user:
                        review.user = user
                    else:
                        raise ValueError(f"User with ID '{value}' not found")
                elif key == 'place_id':
                    place = self.place_repository.get(value)
                    if place:
                        review.place = place
                    else:
                        raise ValueError(f"Place with ID '{value}' not found")
                else:
                    raise ValueError(f"Invalid attribute '{key}' for Review")
            self.review_repository.update(review_id, review_data)
            return review
        return None

    def delete_review(self, review_id):
        """Delete a review by its unique ID."""
        return self.review_repository.delete(review_id)

    def get_reviews_by_place(self, place_id):
        """Get all reviews associated with a specific place."""
        return [
            review for review in self.review_repository.get_all()
            if review.place.id == place_id
        ]

hbnb_facade = HBnBFacade()
