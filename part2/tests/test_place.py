import pytest
from app.models.user import User
from app.models.place import Place  # Make sure to import Place


def test_user_creation():
    user = User(first_name="John", last_name="Doe",
                email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")


def test_place_creation_with_invalid_owner():
    with pytest.raises(ValueError) as excinfo:
        place = Place(title="Invalid Place", description="This should fail",
                      price=100, latitude=37.7749, longitude=-122.4194, owner=None)
    assert str(excinfo.value) == "Owner must be an instance of User."
    print("Invalid owner test passed!")


# Call to the test functions can be omitted as pytest will automatically find them
# when you run pytest in the command line.

# Uncomment the following lines if you want to execute the tests directly without pytest:
test_user_creation()
test_place_creation_with_invalid_owner()
