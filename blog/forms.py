from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, ValidationError
from wtforms import BooleanField
from flask_wtf.file import  FileAllowed, FileField
from wtforms.validators import DataRequired, Length
from wtforms.validators import Email, EqualTo, regexp
from blog.models import User


class RegistratoinForm(FlaskForm):
    image = FileField('Profile photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'],
                            message='Dont forget Avatar!')
                            ])      #here
    name = StringField('name', validators=[
                            DataRequired(), Length(min=4, max=64,
                             message="Pease write down your name!")
                            ])
    username = StringField('Username', validators=[
                            DataRequired(), Length(min=4, max=32,
                            message='Enter more than 4 character!')
                            ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[
                                    DataRequired(), EqualTo('password',
                                     message="Psswords are not Equal!")
                                    ])

    def validate_username(self, username):
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('This username is already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('This email is already exists') 

    def validate_name(self, name):
        user = User.query.filter_by(name= name.data).first()
        if user:
            raise ValidationError('This name is already exists')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                            DataRequired(), Length(min=4, max=25)
                            ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
