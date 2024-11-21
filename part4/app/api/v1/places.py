from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

logger = logging.getLogger(__name__)

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
    'owner_id': fields.String(required=False,
                              description='Owner ID of the place',
                              example='owner_12345')
})

# Define the place update model (only modifiable fields)
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(required=True,
                           description='Updated title of the place',
                           example='Luxury Apartment'),
    'description': fields.String(
        required=True,
        description='Updated description of the place',
        example='A luxury apartment in the heart of the city'
    ),
    'price': fields.Float(required=True,
                          description='Updated price per night',
                          example=200.0),
    'latitude': fields.Float(required=True,
                             description='Updated latitude of the place',
                             example=37.7749),
    'longitude': fields.Float(required=True,
                              description='Updated longitude of the place',
                              example=-122.4194)
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Action not allowed')
    @jwt_required()
    def post(self):
        """Create a new place."""
        current_user = get_jwt_identity()
        place_data = api.payload
        logger.info(f"Payload received: {place_data}")

        try:
            place_data['owner_id'] = current_user['id']  # check if owner_id is present
            place = facade.create_place(place_data)
            return place.to_dict(), 201
        except ValueError as e:
            logger.error(f"ValueError: {str(e)}")
            return {'error': str(e)}, 400
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return {'message': str(e)}, 500 

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()
            return [place.to_dict() for place in places], 200
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
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
            logger.error(f"Exception: {str(e)}")
            return {'message': str(e)}, 500

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Action not allowed')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        place_data = api.payload
        logger.info(f"PUT request data: {place_data}")

        try:
            place = facade.get_place(place_id)

            if not place:
                return {'error': 'Place not found'}, 404
            
            if place.owner_id != current_user['id']:
                return {'error': 'Action not allowed'}, 403

            updated_place = facade.update_place(place_id, place_data)
            if updated_place:
                return updated_place.to_dict(), 200
            else:
                return {'error': 'Place not found'}, 404

        except KeyError as e:
            logger.error(f"KeyError: {str(e)}")
            return {'error': f'Missing required field: {str(e)}'}, 400
        except ValueError as e:
            logger.error(f"ValueError: {str(e)}")
            return {'error': str(e)}, 400
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return {'message': str(e)}, 500
