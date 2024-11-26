from app.models.user import User
from app.models.review import Review
from app.models.place import Place


def test_review_creation():
    # Create an instance of User for the test
    user = User(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="securepassword"
    )

    # Create an instance of Place for the test
    place = Place(
        title="Test Place",
        description="A beautiful place to stay.",
        price=100.0,
        latitude=37.7749,
        longitude=-122.4194,
        owner=user
    )

    # Create an instance of Review
    review = Review(text="Great place!", rating=5, place=place, user=user)

    # Verify that the attributes are correctly defined
    assert review.text == "Great place!"
    assert review.rating == 5
    assert review.place == place
    assert review.user == user
    print("Review creation test passed!")


def test_set_text():
    user = User(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="securepassword"
    )
    place = Place(
        title="Test Place",
        description="A beautiful place to stay.",
        price=100.0,
        latitude=37.7749,
        longitude=-122.4194,
        owner=user
    )
    review = Review(text="Great place!", rating=5, place=place, user=user)

    review.set_text("Amazing place!")
    assert review.text == "Amazing place!"
    print("Set text test passed!")


def test_set_rating():
    user = User(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="securepassword"
    )
    place = Place(
        title="Test Place",
        description="A beautiful place to stay.",
        price=100.0,
        latitude=37.7749,
        longitude=-122.4194,
        owner=user
    )
    review = Review(text="Great place!", rating=5, place=place, user=user)

    review.set_rating(4)
    assert review.rating == 4
    print("Set rating test passed!")


# Run the tests
test_review_creation()
test_set_text()
test_set_rating()
