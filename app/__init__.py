import queue

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

# Application creation
app = Flask(__name__)
# Loading plugins
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
# Load configuration
app.config.from_object('config')

# Task queue handling
tasks = queue.Queue()
task_count = 0
full_task_list = []

from app import views
