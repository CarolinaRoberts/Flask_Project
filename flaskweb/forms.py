from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, NumberRange
from flask_login import current_user
from flaskweb.models import User
from flask_wtf.file import FileField, FileAllowed

class Registration(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                        validators=[DataRequired(), Regexp('^.{6,20}$', message='Your password should be between 6 and 8 characters long.')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose another.')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please choose another.')

class Login(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccount(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken. Please choose another.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is taken. Please choose another.')


class Checkout(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=([DataRequired(), Email()]))
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    county = StringField('County', validators=[DataRequired()])
    post_code =StringField('Post Code',validators=[DataRequired(), Length(min=6, max=8)])
    name_card = StringField('Name on Card', validators=[DataRequired()])
    card_num = IntegerField('Credit Card Number',validators=[DataRequired(), NumberRange(16)])
    exp_date = DateField('Expiry Date', validators=[DataRequired()], format='%d/%m/%Y')
    cvv = IntegerField('CVV', validators=[DataRequired(), NumberRange(3)])
    remember = BooleanField('Shipping address same as billing')
    submit = SubmitField('Confirm Payment')
