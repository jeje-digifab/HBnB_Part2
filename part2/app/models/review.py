from app.models.BaseModel import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        """Initialize a Review instance.

        Args:
            text (str): The text content of the review.
            rating (int): The rating given to the place (1-5).
            place (Place): The Place instance associated with the review.
            user (User): The User instance that wrote the review.

        Raises:
            ValueError: If the user or place is not of the correct type.
        """
        super().__init__()

        if not isinstance(user, User):
            raise ValueError("User must be an instance of User.")

        if not isinstance(place, Place):
            raise ValueError("Place must be an instance of Place.")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def to_dict(self):
        """Convert the Review instance to a dictionary."""
        review_dict = {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id,
            'place_id': self.place.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            '__class__': self.__class__.__name__
        }
        return review_dict

    def set_text(self, text):
        """Set the text of the review.

        Args:
            text (str): The new text of the review.

        Raises:
            ValueError: If the provided text is not a string.
        """
        if not isinstance(text, str):
            raise ValueError("The text must be a string.")
        self.text = text
        self.save()

    def set_rating(self, rating):
        """Set the rating of the review.

        Args:
            rating (int or float): The new rating of the review (1-5).

        Raises:
            ValueError: If the rating is not valid.
        """
        if not isinstance(rating, (int, float)):
            raise ValueError("The rating must be an integer or float.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        self.rating = rating
        self.save()
