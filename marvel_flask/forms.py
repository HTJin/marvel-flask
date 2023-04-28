from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField()
    
class RegisterForm(FlaskForm):
    username = StringField('Create username:', validators=[DataRequired(), Length(min=3, max=40)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Create password:', validators=[DataRequired(), EqualTo('confirm', message='passwords are not matching')])
    confirm = PasswordField('Confirm password:', validators=[DataRequired(), EqualTo('password', message='passwords are not matching')])
    submit = SubmitField()