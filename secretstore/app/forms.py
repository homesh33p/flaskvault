from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired

from wtforms import PasswordField, BooleanField,ValidationError
from wtforms.validators import Length, Email,Regexp, EqualTo

from .models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
    DataRequired(), Length(1, 16),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
    'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):    
    username = StringField('Username', validators=[
    DataRequired(), Length(1, 16),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
    'Usernames must have only letters, numbers, dots or underscores')])
    
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 16),EqualTo('password2', message='Passwords must match.')])
    
    password2 = PasswordField('Confirm password', validators=[DataRequired(),Length(1, 16)])
    
    submit = SubmitField('Register')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')