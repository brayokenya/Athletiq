class Config:

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://nabalayo:karitie@localhost/sports'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}