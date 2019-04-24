from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User
from flask_login import current_user


