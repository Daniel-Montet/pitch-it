from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User
from flask_login import current_user

class Register(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),
                        Length(min=2, max=20)],)
    email = StringField('Email',validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self,email):
            if User.query.filter_by(email = email.data).first():
                raise ValidationError('There is an account with that email')

    def validate_username(self,username):
        if User.query.filter_by(username = username.data).first():
            raise ValidationError('That username is taken')

class Login(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccount(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),
                        Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:   
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username already taken')

    def validate_email(self, email):
        if username.data != current_user.username:
            email = User.query.filter_by(email = email.data).first()
            if email:
                raise ValidationError('Email already taken')