from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, SubmitField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[Length(min=4, max=60)])
    username = StringField('Username', validators=[Length(min=4, max=25)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password',validators=[EqualTo('password')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AccountForm(FlaskForm):
    CHOICES=[
        ('avatar1.jpg','Avatar 1'),
        ('avatar2.jpg','Avatar 2'), 
        ('avatar3.jpg','Avatar 3'), 
        ('avatar4.jpg','Avatar 4'),
        ('avatar5.jpg','Avatar 5'),
        ('avatar6.jpg','Avatar 6')
        ]    
    username = StringField('Username', validators=[Length(min=4, max=25)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    avatar = RadioField('Avatar', choices=CHOICES)
    submit = SubmitField('Submit')
