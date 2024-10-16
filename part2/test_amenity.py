import unittest
from app.models.amenity import Amenity

class TestAmenity(unittest.TestCase):
    def test_amenity_initialization(self):
        amenity = Amenity(name="Pool")
        self.assertEqual(amenity.name, "Pool")
        self.assertIsNotNone(amenity.id)
        self.assertIsNotNone(amenity.created_at)
        self.assertIsNotNone(amenity.updated_at)

    def test_set_name_valid(self):
        amenity = Amenity(name="Gym")
        amenity.set_name("Spa")
        self.assertEqual(amenity.name, "Spa")

    def test_set_name_invalid_type(self):
        amenity = Amenity(name="Gym")
        with self.assertRaises(ValueError):
            amenity.set_name(123)

    def test_set_name_empty(self):
        amenity = Amenity(name="Gym")
        with self.assertRaises(ValueError):
            amenity.set_name("")

    def test_set_name_too_long(self):
        amenity = Amenity(name="Gym")
        with self.assertRaises(ValueError):
            amenity.set_name("a" * 51)

    def test_set_description_valid(self):
        amenity = Amenity(name="Gym")
        amenity.set_description("A place to workout")
        self.assertEqual(amenity.description, "A place to workout")

    def test_set_description_too_long(self):
        amenity = Amenity(name="Gym")
        with self.assertRaises(ValueError):
            amenity.set_description("a" * 256)

    def test_repr(self):
        amenity = Amenity(name="Gym")
        amenity.set_description("A place to workout")
        repr_str = repr(amenity)
        self.assertIn("Amenity(id=", repr_str)
        self.assertIn("name=Gym", repr_str)
        self.assertIn("description=A place to workout", repr_str)

if __name__ == "__main__":
    unittest.main()