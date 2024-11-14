from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

load_dotenv('.env')


def create_app(config_class="config.DevelopmentConfig"):
    """App configuration"""
    app = Flask(__name__)

    app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    """initialize extensions with the app"""
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    """create the API"""
    api = Api(app, version='1.0', title='Your API Title',
              description='API description')

    from app.api.v1.users import api as users_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    """create database tables"""
    with app.app_context():
        db.create_all()

    return app
