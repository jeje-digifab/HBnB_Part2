from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        data = api.payload  # Get the request payload
        print(f"Payload received: {data}")  # Debug to check the payload

        try:
            new_review = facade.create_review(data)  # Create the review using the facade
            return {'message': 'Review created', 'review': new_review.to_dict()}, 201  # Convert to dict
        except KeyError as e:
            return {'message': f'Missing required field: {str(e)}'}, 400
        except Exception as e:
            return {'message': str(e)}, 500


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()  # Get all reviews using the facade
            return {'reviews': [review.to_dict() for review in reviews]}, 200  # Convert to dict
        except Exception as e:
            return {'message': str(e)}, 500

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)  # Get review by ID
            if review:
                return {'review': review.to_dict()}, 200  # Convert to dict
            else:
                return {'message': 'Review not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload  # Get the updated data
        try:
            updated_review = facade.update_review(review_id, data)  # Update review using the facade
            if updated_review:
                return {'message': 'Review updated', 'review': updated_review.to_dict()}, 200  # Convert to dict
            else:
                return {'message': 'Review not found'}, 404
        except KeyError as e:
            return {'message': f'Missing required field: {str(e)}'}, 400
        except Exception as e:
            return {'message': str(e)}, 500

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            if facade.delete_review(review_id):
                return {'message': 'Review deleted'}, 200
            else:
                return {'message': 'Review not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found or no reviews available')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)  # Get reviews by place ID
            if reviews:
                return {'reviews': [review.to_dict() for review in reviews]}, 200  # Convert to dict
            else:
                return {'message': 'Place not found or no reviews available'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
