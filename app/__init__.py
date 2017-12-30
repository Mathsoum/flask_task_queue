import queue

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')
tasks = queue.Queue()
task_count = 0
full_task_list = []

from app import views
