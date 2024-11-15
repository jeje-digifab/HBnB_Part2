from app.models.BaseModel import BaseModel
from app.models.user import User
from app.models.place import Place
from app import db


class Review(BaseModel, db.Model):
    """
    Represents a review in the application.

    Inherits from BaseModel, which provides common attributes:
    - id: Unique identifier for the review.
    - created_at: Timestamp when the review is created.
    - updated_at: Timestamp when the review is last updated.

    Attributes:
    - text (str): The text of the review.
    - rating (int): The rating given to the place (1-5).
    - user_id (str): The ID of the user who wrote the review.
    - place_id (str): The ID of the place being reviewed.
    """
    __tablename__ = 'review'

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey(
        'user.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey(
        'place.id'), nullable=False)

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

    def update_review(self, review_data):
        """Update the review with the provided data.

        Args:
            review_data (dict): A dictionary containing the attributes to update.

        Raises:
            ValueError: If the provided review_data is not a dictionary or if it
                        contains invalid fields.
        """
        if not isinstance(review_data, dict):
            raise ValueError("review_data must be a dictionary")

        for key, value in review_data.items():
            if hasattr(self, key):
                # Update the attribute with the new value
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid attribute '{key}' for Review")
        self.save()  # Save the changes after updating

    def delete(self):
        """Delete the review instance from the repository."""
        if self.review_repo.delete(self.id):
            return True
        return False
