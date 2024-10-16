from app.models.BaseModel import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not isinstance(user, User):
            raise ValueError("User must be an instance of User.")

        if not isinstance(place, Place):
            raise ValueError("Place must be an instance of Place.")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def set_text(self, text):
        if not isinstance(text, str):
            raise ValueError("The text must be a string.")

        self.text = text
        self.save()

    def set_rating(self, rating):
        if not isinstance(rating, (int, float)):
            raise ValueError("The rating must be an integer or float.")

        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")

        self.rating = rating
        self.save()
