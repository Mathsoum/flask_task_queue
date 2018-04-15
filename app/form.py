from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    command = StringField(id='command', label='Command', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField(id='login', label='Login', validators=[DataRequired()])
    password = PasswordField(id='password', label='Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
