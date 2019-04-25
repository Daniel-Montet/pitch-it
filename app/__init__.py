from flask import Flask
from flask import Blueprint
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view='main.home'
login_manager.login_message_category='info'


mail = Mail()


def create_app(config_name):
    app= Flask(__name__)
    app.config.from_object(config_options[config_name])
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from app.users.routes import users
    from app.posts.routes import posts
    from app.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    

    return app