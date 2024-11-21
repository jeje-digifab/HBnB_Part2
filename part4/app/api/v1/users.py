from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

"""
Define the user model for input validation and documentation
"""
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user',
                                example='Jane'),
    'last_name': fields.String(required=True,
                               description='Last name of the user',
                               example='Doe'),
    'email': fields.String(required=True,
                           description='Email of the user',
                           example='jane.doe@example.com'),
    'password': fields.String(required=True,
                              description='Password of the user',
                              example='securepassword'),
    'is_admin': fields.Boolean(required=True,
                               description='Is the user an admin?',
                               example=True),
    'is_owner': fields.Boolean(required=True,
                               description='Is the user an owner?',
                               example=True)
})

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
        Create a new user with hashed password.
        """
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(user_data)
        if not user:
            return {'error': 'Failed to create user'}, 400
        return {
            'message': 'User created successfully',
            'user': user.to_dict()
        }, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """
        Retrieve the list of all users.

        This method retrieves all registered users and returns their
        details including `id`, `first_name`, `last_name`, and `email`.
        """
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    """
    Resource for managing an individual user by their ID.
    """

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get a user's details by their ID.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User details updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Action not allowed')
    @jwt_required()
    def put(self, user_id):
        """
        Update a user's details.
        This method allows for updating a user's details like `first_name`,
        `last_name`, and `email` based on the provided `user_id`.
        """
        user_data = api.payload
        current_user = get_jwt_identity()

        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404

            if user.id != current_user['id']:
                return {'error': 'Action not allowed'}, 403
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            if 'password' in user_data:
                return {'error': "You cannot update the password."}, 403

            return updated_user.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500
