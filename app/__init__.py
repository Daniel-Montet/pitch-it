from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__) 
app.config['SECRET_KEY']='fe80d26ee9e9e49b181c65aee655938c'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
db = SQLAlchemy(app)

from app import views
