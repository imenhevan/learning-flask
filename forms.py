from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import InputRequired, Email, Length

class SignupForm(Form):
	first_name=StringField('First name', validators=[InputRequired("Please enter your first name.")])
	last_name=StringField('Last name', validators=[InputRequired(message='Please enter your last name.')])
	dob=StringField('Date of Birth', validators=[InputRequired(message='Please enter your birthday.')])
	email=StringField('Email', validators=[InputRequired(message='Please enter your email address.'), Email("Please enter a valid email.")])
	password = PasswordField('Password', validators=[InputRequired(message='Please enter your password.'), Length(min=6, message="Passwords must be 6 characters or more.")])
	submit = SubmitField('Sign up')

class LoginForm(Form):
	email=StringField('Email', validators=[InputRequired(),Email("Please enter your email address.")])
	password=PasswordField('Password', validators=[InputRequired()])
	submit=SubmitField("Sign in")

class AddressForm(Form):
	address=StringField('Address', validators=[InputRequired(),Email("Please enter a address.")])
	submit=SubmitField("Search")
