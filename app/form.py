from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    message = StringField(id='message', label='New task message', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField(id='login', label='Login', validators=[DataRequired()])
    password = PasswordField(id='password', label='Password', validators=[DataRequired()])
