class Config:

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://nabalayo:karitie@localhost/sports'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '1738'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}