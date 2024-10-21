from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
import os
from dotenv import load_dotenv

load_dotenv('.env')


def create_app():
    """app configuration"""
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API',
            description='HBnB Application API')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

    jwt = JWTManager(app)

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app

    """from app.api.v1 import users, places, reviews, amenities
    app.register_blueprint(users.bp)
    app.register_blueprint(places.bp)
    app.register_blueprint(reviews.bp)
    app.register_blueprint(amenities.bp)"""
    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews,
    # and amenities will be added later
