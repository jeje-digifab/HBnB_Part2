from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade

api = Namespace('reviews', description='Review operations')

# Define the models for related entities
user_model = api.model('ReviewUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the reviewer'),
    'last_name': fields.String(description='Last name of the reviewer'),
    'email': fields.String(description='Email of the reviewer')
})

place_model = api.model('ReviewPlace', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
})

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the reviewer'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'user': fields.Nested(user_model, description='Reviewer details'),
    'place': fields.Nested(place_model, description='Place details')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        data = api.payload
        try:
            new_review = facade.create_review(data)
            return {'message': 'Review created', 'review': new_review.to_dict()}, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()
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
            review = facade.get_review(review_id)
            if review:
                return {'review': review.to_dict()}, 200
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
        data = api.payload
        try:
            updated_review = facade.update_review(review_id, data)
            if updated_review:
                return {'message': 'Review updated', 'review': updated_review.to_dict()}, 200
            else:
                return {'message': 'Review not found'}, 404
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 500
