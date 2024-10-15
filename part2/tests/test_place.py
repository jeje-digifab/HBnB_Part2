import pytest
from app.models.place import Place
from app.models.user import User
from app.models.review import Review


def test_place_creation():
    """
    Test the creation of a Place object and its relationship with a Review and a User object.

    This test checks that:
    - A Place object is correctly created with the provided attributes.
    - A Review object can be associated with a Place.
    - The relationship between Place and Review works as expected.
    """
    # Create a user (owner of the place)
    owner = User(first_name="Alice", last_name="Smith",
                 email="alice.smith@example.com")

    # Create a place with given details and an owner
    place = Place(title="Cozy Apartment", description="A nice place to stay",
                  price=100, latitude=37.7749, longitude=-122.4194, owner=owner)

    # Create a review associated with the place and the user owner
    review = Review(text="Great stay!", rating=5, place=place, user=owner)

    # Add the review to the place
    place.add_review(review)

    # Assertions to verify the attributes are correctly initialized
    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Place creation and relationship test passed!")


def test_place_creation_with_invalid_owner():
    """
    Test the creation of a Place object with an invalid owner (None).

    This test checks that:
    - Creating a Place without a valid owner raises a ValueError.
    - The error message matches the expected value.
    """
    # Use pytest to check that the exception is raised
    with pytest.raises(ValueError) as excinfo:
        place = Place(title="Invalid Place", description="This should fail",
                      price=100, latitude=37.7749, longitude=-122.4194, owner=None)

    # Verify that the error message matches
    assert str(excinfo.value) == "Owner must be an instance of User."
    print("Invalid owner test passed!")
