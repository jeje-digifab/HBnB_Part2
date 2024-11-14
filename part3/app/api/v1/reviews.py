from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

logger = logging.getLogger(__name__)

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model(
    'Review',
    {
        'text': fields.String(
            required=True,
            description='Text of the review',
            example='Great place to stay!'
        ),
        'rating': fields.Integer(
            required=True,
            description='Rating of the place (1-5)',
            example=4
        ),
        'user_id': fields.String(
            required=True,
            description='ID of the user',
            example='user_12345'
        ),
        'place_id': fields.String(
            required=True,
            description='ID of the place',
            example='place_67890'
        )
    }
)

# Define the review update model (only modifiable fields)
review_update_model = api.model(
    'ReviewUpdate',
    {
        'text': fields.String(
            required=True,
            description='Updated text of the review',
            example='Amazing place to stay!'
        ),
        'rating': fields.Integer(
            required=True,
            description='Updated rating of the place (1-5)',
            example=5
        )
    }
)

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Action not allowed')
    @jwt_required()
    def post(self):
        """Register a new review"""
        data = api.payload
        current_user = get_jwt_identity()
        logger.info(f"Payload received: {data}")

        try:
            place_id = data.get('place_id')  # check if place_id is provided
            place = facade.get_place(place_id)  # check if place exists
            if place is None:
                return {'message': 'Place not found'}, 404
            
            if place.owner_id == current_user['id']:  # Check if the user is the owner of the place
                return {'message': 'Action not allowed: You cannot review your own place'}, 403
            existing_review = facade.get_review_by_user_and_place(current_user['id'], place_id)  # Check if the user has already reviewed the place
            if existing_review:
                return {'message': 'Action not allowed: You have already reviewed this place'}, 403
            
            new_review = facade.create_review(data)
            return {
                'message': 'Review created',
                'review': new_review.to_dict()
            }, 201
        except KeyError as e:
            logger.error(f"KeyError: {str(e)}")
            return {
                'message': f'Missing required field: {str(e)}'
            }, 400
        except ValueError as e:
            logger.error(f"ValueError: {str(e)}")
            return {'message': str(e)}, 400
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return {'message': str(e)}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()
            return {
                'reviews': [review.to_dict() for review in reviews]
            }, 200
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return {'message': str(e)}, 500

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            if review:
                return {'review': review.to_dict()}, 200
            else:
                return {'message': 'Review not found'}, 404
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return {'message': str(e)}, 500

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Action not allowed')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload
        current_user = get_jwt_identity()
        logger.info(f"PUT request data: {data}")

        try:
            review = facade.get_review(review_id)  # Get the review by ID
            if review is None:
                return {'message': 'Review not found'}, 404
            
            if review.user_id != current_user['id']:  # Check if the user is the owner of the review
                return {'message': 'Action not allowed'}, 403

            updated_review = facade.update_review(review_id, data)
            if updated_review:
                return {
                    'message': 'Review updated',
                    'review': updated_review.to_dict()
                }, 200
            else:
                return {'message': 'Review not found'}, 404
        except KeyError as e:
            logger.error(f"KeyError: {str(e)}")
            return {
                'message': f'Missing required field: {str(e)}'
            }, 400
        except ValueError as e:
            logger.error(f"ValueError: {str(e)}")
            return {'message': str(e)}, 400
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return {'message': str(e)}, 500

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Action not allowed')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        logger.info(f"DELETE request for review_id: {review_id}")
        current_user = get_jwt_identity()
        try:
            review = facade.get_review(review_id)  # Get the review by ID
            if review is None:
                return {'message': 'Review not found'}, 404
            
            if review.user_id != current_user['id']:  # Check if the user is the owner of the review
                return {'message': 'Action not allowed'}, 403
            
            if facade.delete_review(review_id):
                return {'message': 'Review deleted successfully'}, 200
            else:
                return {'message': 'Review not found'}, 404
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return {'message': str(e)}, 500

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found or no reviews available')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            if reviews:
                return {
                    'reviews': [review.to_dict() for review in reviews]
                }, 200
            else:
                return {'message': 'Place not found or no reviews available'}, 404
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return {'message': str(e)}, 500
