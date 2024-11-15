from app.models.BaseModel import BaseModel
from app.models.user import User
from app import db
from app.models.place_amenity import place_amenity

class Place(BaseModel, db.Model):
    """
    Represents a place in the application.

    Inherits from BaseModel, which provides common attributes:
    - id: Unique identifier for the place.
    - created_at: Timestamp when the place is created.
    - updated_at: Timestamp when the place is last updated.

    Attributes:
    - title (str): The title of the place. Must not exceed 100 characters.
    - description (str): A detailed description of the place (optional).
    - price (float): The price per night for the place.
        Must be a positive value.
    - latitude (float): Latitude coordinate for the place location.
        Must be between -90.0 and 90.0.
    - longitude (float): Longitude coordinate for the place location.
        Must be between -180.0 and 180.0.
    - owner (User): Instance of User who owns the place.
        Must be a valid User instance.
    - reviews (list): A list to store related reviews.
    - amenities (list): A list to store related amenities.
    """
    __tablename__ = 'place'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places', lazy=True)

    def __init__(self, title, description, price, latitude, longitude, owner: User):
        """
        Initializes a new instance of the Place class.

        Parameters:
            title (str): The title of the place.
            description (str): A brief description of the place.
            price (float): The price per night for renting the place.
            latitude (float): The geographical latitude of the place.
            longitude (float): The geographical longitude of the place.
            owner (User): An instance of the User class representing
                the owner of the place.

        Raises:
            ValueError: If the owner is not an instance of User.
        """
        super().__init__()

        if not isinstance(owner, User):
            raise ValueError("Owner must be an instance of User.")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def to_dict(self):
        """complete method to serialize obj"""
        place_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id,
            "amenities": [amenity.id for amenity in self.amenities],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "__class__": self.__class__.__name__
        }
        return place_dict

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def set_title(self, title):
        """Set the title of the place with validation."""
        if not isinstance(title, str):
            return "The title must be a string."

        if len(title) > 100:
            return "The title is too long."
        else:
            self.title = title

    def set_description(self, description):
        """Set the description of the place with validation."""
        if not isinstance(description, str):
            return "The description must be a string."
        self.description = description

    def set_price(self, price):
        """Set the price of the place with validation."""
        if not isinstance(price, (int, float)):
            return "The price must be a number."

        if price <= 0:
            return "The price must be positive and not zero."
        else:
            self.price = price

    def set_latitude(self, latitude):
        """Set the latitude of the place with validation."""
        if not isinstance(latitude, (int, float)):
            return "The latitude must be a number."

        if latitude < -90 or latitude > 90:
            return "Latitude is outside the range."

        self.latitude = latitude

    def set_longitude(self, longitude):
        """Set the longitude of the place with validation."""
        if not isinstance(longitude, (int, float)):
            return "The longitude must be a number."

        if longitude < -180 or longitude > 180:
            return "Longitude is outside the range."

        self.longitude = longitude
