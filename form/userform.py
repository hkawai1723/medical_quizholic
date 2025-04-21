from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class RegisterForm(FlaskForm):
    username = StringField(
        'Username', [DataRequired('Please enter user name')])
    email = StringField('Email', [DataRequired(
        'Please enter email'), Email('Please enter proper email address')])
    password = PasswordField(
        'Password', [DataRequired('Please enter password'), Length(min=8, max=16, message='Password must be 8 to 16 characters long.'), Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$', message='Password must contain at least one letter and one number.')])
    password_confirm = PasswordField(
        'Password Confirm', [DataRequired('Please enter password confirm'), EqualTo('password', message='Password Confirm must match with password.')])
    submit = SubmitField('Send')

class UpdateUserForm(FlaskForm):
    username = username = StringField(
        'Username', [DataRequired('Please enter user name')])
    submit = SubmitField('Update')

class LoginForm(FlaskForm):
    email = StringField(
        'Email', [DataRequired('Please enter email.'), Email()])
    password = PasswordField(
        'Password', [DataRequired('Please enter password.')])
    submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('New password', validators=[DataRequired(),])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(),EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Change Password')