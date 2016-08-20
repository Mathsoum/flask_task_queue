import queue

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
tasks = queue.Queue()
task_count = 0
full_task_list = []

from app import views
