from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class TaskForm(Form):
    message = StringField('message', validators=[DataRequired()])
