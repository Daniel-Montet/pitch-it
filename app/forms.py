from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError,Required
from app.models import User

class Register(FlaskForm):
    username = StringField('Username',validators=[Required(),
                        Length(min=2, max=20)])
    email = StringField('Email',validators=[Required(),Email()])

    password = PasswordField('Password', validators=[Required()])
    confirm_password = PasswordField('Confirm Password', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username already taken')

    def validate_username(self, email):
        email = User.query.filter_by(username = email.data).first()
        if email:
            raise ValidationError('Email already taken')

class Login(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
