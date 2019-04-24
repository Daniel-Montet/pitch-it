import os

class Config:
    SECRET_KEY='fe80d26ee9e9e49b181c65aee655938c'
    SQLALCHEMY_DATABASE_URI= 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "dmontetproff@gmail.com"
    MAIL_PASSWORD = "dominuslew"

class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}