import os

class Config:
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOADED_PHOTOS_DEST ='app/static/photos'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_DEV')
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}