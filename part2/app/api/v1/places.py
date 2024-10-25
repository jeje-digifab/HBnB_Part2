from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade

api = Namespace('places', description='Place related operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True,
                           description='The title of the place',
                           example='Cozy Apartment'),
    'description': fields.String(
        required=True,
        description='Description of the place',
        example='A cozy apartment in the heart of the city'
    ),
    'price': fields.Float(required=True,
                          description='Price per night',
                          example=100.0),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place',
                             example=37.7749),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place',
                              example=-122.4194),
    'owner_id': fields.String(required=True,
                              description='Owner ID of the place',
                              example='owner_12345')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place."""
        place_data = api.payload
        try:
            place = facade.create_place(place_data)
            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()
            return [place.to_dict() for place in places], 200
        except Exception as e:
            return {'message': str(e)}, 500


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            # Fetch place by ID
            place = facade.get_place(place_id)
            if place:
                # Return the place details
                return {'place': place.to_dict()}, 200
            else:
                # Return not found message
                return {'message': 'Place not found'}, 404
        except Exception as e:
            # Return error message
            return {'message': str(e)}, 500

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        try:
            updated_place = facade.update_place(place_id, place_data)
            if updated_place:
                return updated_place.to_dict(), 200
            else:
                return {'error': 'Place not found'}, 404
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 500
