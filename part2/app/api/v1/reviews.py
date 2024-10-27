from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True,
                          description='Text of the review',
                          example='Great place to stay!'),
    'rating': fields.Integer(required=True,
                             description='Rating of the place (1-5)',
                             example=4),
    'user_id': fields.String(required=True,
                             description='ID of the user',
                             example='user_12345'),
    'place_id': fields.String(required=True,
                              description='ID of the place',
                              example='place_67890')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        # Get the request payload
        data = api.payload
        # Debug to check the payload
        print(f"Payload received: {data}")

        try:
            # Create the review using the facade
            new_review = facade.create_review(data)
            # Convert to dict
            return {'message': 'Review created',
                    'review': new_review.to_dict()}, 201
        except KeyError as e:
            return {'message': f'Missing required field: {str(e)}'}, 400
        except Exception as e:
            return {'message': str(e)}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            # Get all reviews using the facade
            reviews = facade.get_all_reviews()
            # Convert to dict
            return {'reviews': [review.to_dict() for review in reviews]}, 200
        except Exception as e:
            return {'message': str(e)}, 500


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            # Get review by ID
            review = facade.get_review(review_id)
            if review:
                # Convert to dict
                return {'review': review.to_dict()}, 200
            else:
                return {'message': 'Review not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Get the updated data
        data = api.payload
        try:
            # Update review using the facade
            updated_review = facade.update_review(review_id, data)
            if updated_review:
                # Convert to dict
                return {'message': 'Review updated', 'review': updated_review.to_dict()}, 200
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
            # Get reviews by place ID
            reviews = facade.get_reviews_by_place(place_id)
            if reviews:
                # Convert to dict
                return {
                    'reviews': [
                        review.to_dict()
                        for review in reviews
                    ]
                }, 200
            else:
                return {
                    'message': 'Place not found or no reviews available'
                }, 404
        except Exception as e:
            return {'message': str(e)}, 500
