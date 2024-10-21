from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user')
})

facade = HBnBFacade()


@api.route('/')
class UserList(Resource):
    """
    Resource for managing the collection of users.

    Contains methods for:
    - Creating a new user (POST)
    - Retrieving the list of all users (GET)
    """

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new user.

        This method expects a JSON payload containing `first_name`,
        `last_name`, `email`, and `password`. It checks if the email
        is already registered. If not, it creates a new user and
        returns the user details.

        Returns:
            dict: The created user data with `id`,
                `first_name`, `last_name`, and `email`.
            HTTP Status Code 201: User created.
            HTTP Status Code 400: If email already registered or
                input data is invalid.
        """
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(user_data)
        if not user:
            return {'error': 'Failed to create user'}, 400
        return {'id': user.id, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email}, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """
        Retrieve the list of all users.

        This method retrieves all registered users and returns their
        details including `id`, `first_name`, `last_name`, and `email`.

        Returns:
            list: A list of user objects.
            HTTP Status Code 200: Users retrieved successfully.
        """
        users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': user.email} for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    """
    Resource for managing an individual user by their ID.

    Contains methods for:
    - Retrieving a user by ID (GET)
    - Updating a user by ID (PUT)
    """

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get a user's details by their ID.

        This method fetches the user with the given `user_id` and returns
        their details, including `id`, `first_name`, `last_name`, and `email`.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            dict: The user's data.
            HTTP Status Code 200: User found and returned.
            HTTP Status Code 404: If user with the given ID does not exist.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User details updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """
        Update a user's details.

        This method allows for updating a user's details like `first_name`,
        `last_name`, and `email` based on the provided `user_id`.

        Args:
            user_id (str): The unique identifier of the user.
            user_data (dict): A JSON payload with updated user data.

        Returns:
            dict: The updated user data.
            HTTP Status Code 200: User updated successfully.
            HTTP Status Code 404: If user with the given ID does not exist.
            HTTP Status Code 400: If input data is invalid.
        """
        user_data = api.payload
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {'id': updated_user.id, 'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email}, 200
