from flask import render_template
from flask import request

from app import app, tasks, full_task_list
from app.form import TaskForm
from app.runner import Task


@app.route('/')
def hello_world():
    return render_template("main.html")


@app.route('/add', methods=['POST', 'GET'])
def add_task():
    if request.method == 'POST':
        if request.form['message'] != '':
            tasks.put(Task(request.form['message']))

    form = TaskForm()
    return render_template("addition.html", form=form, full_task_list=full_task_list)
