from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade

api = Namespace('amenities', description='Amenity related operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(
        required=True,
        description='The name of the amenity',
        example='Wi-Fi'
    ),
    'description': fields.String(
        required=True,
        description='Description of the amenity',
        example='High-speed internet access'
    )
})


@ api.route('/')
class AmenityList(Resource):
    @ api.expect(amenity_model, validate=True)
    @ api.response(201, 'Amenity successfully created')
    @ api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity."""
        amenity_data = api.payload
        try:
            amenity = facade.create_amenity(amenity_data)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @ api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            amenities = facade.get_all_amenities()
            return [amenity.to_dict() for amenity in amenities], 200
        except Exception as e:
            return {'message': str(e)}, 500


@ api.route('/<amenity_id>')
class AmenityResource(Resource):
    @ api.response(200, 'Amenity details retrieved successfully')
    @ api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)  # Fetch amenity by ID
            if amenity:
                # Return the amenity details
                return {'amenity': amenity.to_dict()}, 200
            else:
                # Return not found message
                return {'message': 'Amenity not found'}, 404
        except Exception as e:
            # Return error message
            return {'message': str(e)}, 500

    @ api.expect(amenity_model, validate=True)
    @ api.response(200, 'Amenity updated successfully')
    @ api.response(404, 'Amenity not found')
    @ api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if updated_amenity:
                return updated_amenity.to_dict(), 200
            else:
                return {'error': 'Amenity not found'}, 404
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 500
