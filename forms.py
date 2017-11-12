from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import TextField


class RegistrationForm(FlaskForm):
	email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
	password = PasswordField('password', validators=[validators.DataRequired(), validators.length(min=8, message='Please choose password of at least 8 characters')])
	password2 = PasswordField('password2', validators=[validators.DataRequired(), validators.EqualTo('password', message='passwords must match')])
	submit = SubmitField('Submit', validators=[validators.DataRequired()])

class LoginForm(FlaskForm):
	loginemail = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
	loginpassword = PasswordField('password', validators=[validators.DataRequired(message="Password field is required")])
	submit = SubmitField('submit', validators=[validators.DataRequired()])

class AddLinkForm(FlaskForm):
	link = TextField('linkform', validators=[validators.DataRequired()])
	submit = SubmitField('addlink', validators=[validators.DataRequired()])

