from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade


api = Namespace('places', description='Place related operations')



"""include all necessary fields for cross "place" 
to "Owner" or when a user already exist"""
place_model = api.model('Place', {
    'title': fields.String(required=True, description='The title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='Owner ID of the place'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})



"""
This method handles the creation of a new place via a POST request.
It uses the facade to create the place, manages potential errors, and 
returns either the created place with a success status or 
an error message with a failure status.
"""
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    def post(self):
        """Create a new place."""
        place_data = api.payload
        try:
            place = facade.create_place(place_data)
            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)  # Fetch place by ID
            if place:
                return {'place': place.to_dict()}, 200  # Return the place details
            else:
                return {'message': 'Place not found'}, 404  # Return not found message
        except Exception as e:
            return {'message': str(e)}, 500  # Return error message