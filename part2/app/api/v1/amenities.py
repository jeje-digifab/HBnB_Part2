from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')  # Add description field
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = api.payload  # Get the request payload (data sent in the request)
        try:
            new_amenity = facade.create_amenity(data)  # Pass the whole dictionary
            return {'message': 'Amenity created', 'amenity': new_amenity.to_dict()}, 201  # Convert to dict
        except KeyError as e:
            return {'message': f'Invalid input, "{str(e)}" is required'}, 400  # Specify the missing field
        except Exception as e:
            return {'message': str(e)}, 500

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            amenities = facade.get_all_amenities()  # Use the facade to fetch all amenities
            return {'amenities': [amenity.to_dict() for amenity in amenities]}, 200  # Convert all amenities to dict
        except Exception as e:
            return {'message': str(e)}, 500

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)  # Fetch amenity by ID
            if amenity:
                return {'amenity': amenity.to_dict()}, 200  # Convert to dict
            else:
                return {'message': 'Amenity not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = api.payload  # Get the updated data
        try:
            updated_amenity = facade.update_amenity(amenity_id, data)  # Pass the whole dictionary
            if updated_amenity:
                return {'message': 'Amenity updated', 'amenity': updated_amenity.to_dict()}, 200  # Convert to dict
            else:
                return {'message': 'Amenity not found'}, 404
        except KeyError as e:
            return {'message': f'Invalid input, "{str(e)}" is required'}, 400  # Specify the missing field
        except Exception as e:
            return {'message': str(e)}, 500
