from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from config import config

bcrypt = Bcrypt()
jwt = JWTManager()
load_dotenv('.env')

def create_app(config_name='development'):
    """App configuration"""
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    
    if isinstance(config_name, str) and config_name.startswith('config.'):
        app.config.from_object(config_name)

    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API')

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
