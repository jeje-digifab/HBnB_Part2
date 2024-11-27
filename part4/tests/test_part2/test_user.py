import unittest
from app.models.user import User
from datetime import datetime
from werkzeug.security import check_password_hash

class TestUser(unittest.TestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'is_admin': False,
            'is_owner': False
        }
        self.user = User(**self.user_data)

    def test_user_creation(self):
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertTrue(check_password_hash(self.user.password, self.user_data['password']))
        self.assertEqual(self.user.first_name, self.user_data['first_name'])
        self.assertEqual(self.user.last_name, self.user_data['last_name'])
        self.assertFalse(self.user.is_admin)
        self.assertFalse(self.user.is_owner)
        self.assertIsInstance(self.user.created_at, datetime)
        self.assertIsInstance(self.user.updated_at, datetime)

    def test_become_owner(self):
        self.user.become_owner()
        self.assertTrue(self.user.is_owner)

    def test_add_owned_place(self):
        self.user.become_owner()
        place = type('Place', (object,), {'id': 1})()
        self.user.add_owned_place(place)
        self.assertIn(place, self.user.owned_places)

    def test_add_owned_place_not_owner(self):
        place = type('Place', (object,), {'id': 1})()
        with self.assertRaises(ValueError):
            self.user.add_owned_place(place)

    def test_rent_place(self):
        place = type('Place', (object,), {'id': 1})()
        self.user.rent_place(place)
        self.assertIn(place, self.user.rented_places)

    def test_to_dict(self):
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict['email'], self.user.email)
        self.assertEqual(user_dict['first_name'], self.user.first_name)
        self.assertEqual(user_dict['last_name'], self.user.last_name)
        self.assertEqual(user_dict['is_admin'], self.user.is_admin)
        self.assertEqual(user_dict['is_owner'], self.user.is_owner)
        self.assertEqual(user_dict['owned_places'], [])
        self.assertEqual(user_dict['rented_places'], [])
        self.assertEqual(user_dict['created_at'], self.user.created_at.isoformat())
        self.assertEqual(user_dict['updated_at'], self.user.updated_at.isoformat())
        self.assertNotIn('password', user_dict)

    def test_validate_email(self):
        with self.assertRaises(ValueError):
            User.validate_email('invalid-email')

    def test_validate_name(self):
        with self.assertRaises(ValueError):
            User.validate_name('a' * 51, 'First Name')

    def test_set_password(self):
        self.user.set_password('newpassword')
        self.assertTrue(check_password_hash(self.user.password, 'newpassword'))

    def test_check_password(self):
        self.assertTrue(self.user.check_password('password123'))
        self.assertFalse(self.user.check_password('wrongpassword'))

    def test_update(self):
        new_data = {
            'email': 'new@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'password': 'newpassword'
        }
        self.user.update(new_data)
        self.assertEqual(self.user.email, new_data['email'])
        self.assertEqual(self.user.first_name, new_data['first_name'])
        self.assertEqual(self.user.last_name, new_data['last_name'])

if __name__ == '__main__':
    unittest.main()