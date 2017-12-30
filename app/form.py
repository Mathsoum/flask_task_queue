from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    message = StringField(id='message', label='New task message', validators=[DataRequired()])
