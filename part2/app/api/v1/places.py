from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        data = api.payload
        try:
            new_place = facade.create_place(data)
            return {'message': 'Place created', 'place': new_place.to_dict()}, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()  # Fetch all places from the facade
            return {'places': [place.to_dict() for place in places]}, 200
        except Exception as e:
            return {'message': str(e)}, 500

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            if place:
                return {'place': place.to_dict()}, 200
            else:
                return {'message': 'Place not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload
        try:
            updated_place = facade.update_place(place_id, data)
            if updated_place:
                return {'message': 'Place updated', 'place': updated_place.to_dict()}, 200
            else:
                return {'message': 'Place not found'}, 404
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 500


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
