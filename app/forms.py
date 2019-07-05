from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, Rfi, Team
import os


class RFIForm(FlaskForm):
    team=[('Engineer','Engineer'),('Architect','Architect'),('Landscape Architect','Landscape Architect'), ('Natural','Natural Resources'), ('Cultural','Cultural Resources'), ('PM','Project Manager'),('CM','Construction Manager')]
    rfi_number = StringField('RFI Number: ', validators=[DataRequired()])
    title = StringField('Title: ', validators=[DataRequired()])
    date_received = StringField('Date Submitted: ', validators=[DataRequired()], default='mm/dd/yyyy')
    dwg_refer = StringField('Drawing Reference: ')
    spec_refer = StringField('Specification Reference: ' )
    cost_change = BooleanField('Change in Contract Cost? ')
    time_change = BooleanField('Change in Contract Time? ')
    assigned_to = SelectField('Response Requested From: ', choices = team)
    UploadFile = FileField()
    submit=SubmitField('Submit RFI', render_kw={'class':"w3-button w3-indigo w3-hover-blue"})

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In',render_kw={'class':"w3-button w3-indigo w3-hover-blue"})


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register',render_kw={'class':"w3-button w3-indigo w3-hover-blue"})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ResponseForm(FlaskForm):
	date_response = StringField('Response Date: ', validators=[DataRequired()], default='mm/dd/yyyy')
	reviewer = StringField('Reviewed By: ', validators=[DataRequired()])
	response = TextAreaField('Response', validators=[Length(min=0, max=1000)])
	submit=SubmitField('Submit Response',render_kw={'class':"w3-button w3-indigo w3-hover-blue"})

class TeamForm(FlaskForm):
    team=[('Engineer','Engineer'),('Architect','Architect'),('Landcape Architect','Landscape Architect'), ('Natural','Natural Resources'), ('Cultural','Cultural Resources'), ('PM','Project Manager'),('CM','Construction Manager'),('Contractor','Contractor')]
    role = SelectField('Team Role', choices=team)
    fName = StringField('First Name:')
    lName = StringField('Last Name:')
    email = StringField('Email Address:', validators=[Email()])
    submit = SubmitField('Update Team',render_kw={'class':"w3-button w3-indigo w3-hover-blue"})


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This email address does not belong to a registered user.')

class ProjectForm(FlaskForm):
    unit_name= StringField('Park Name', validators=[DataRequired()])
    proj_title = StringField('Project Title', validators=[DataRequired()])
    submit = SubmitField('Create Project', render_kw={'class':"w3-button w3-indigo w3-hover-blue"})

