import os

class Config:
    """Classe de base pour la configuration de l'application."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    DEBUG = False

class DevelopmentConfig(Config):
    """Configuration pour le développement."""
    DEBUG = True

class ProductionConfig(Config):
    """Configuration pour la production."""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
