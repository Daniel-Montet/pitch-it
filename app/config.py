import os

class Config:
    SECRET_KEY='fe80d26ee9e9e49b181c65aee655938c'
    SQLALCHEMY_DATABASE_URI= 'postgresql+psycopg2://daniel:dominuslew@localhost/pitch'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "dmontetproff@gmail.com"
    MAIL_PASSWORD = "dominuslew1"

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}