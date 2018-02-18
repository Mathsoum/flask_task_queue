import flask
from flask_login import login_user, login_required
import json

import app
from app import app as _app, tasks, full_task_list
from app.form import TaskForm, LoginForm
from app.runner import Task
from app.user import User

import url


def base_template_context():
    nav_form = LoginForm()
    return {'nav_form': nav_form}


@_app.route('/')
def index():
    context = base_template_context()
    context["task_form"] = TaskForm()
    context["full_task_list"] = full_task_list
    if len(full_task_list) > 0:
        context["last_command"] = full_task_list[-1].command
    else:
        context["last_command"] = ""
    return flask.render_template("main.html", **context)


@_app.route('/login', methods=['GET', 'POST'])
def login():
    context = base_template_context()

    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = User.get(u'')
        login_user(user)

        flask.flash('Logged in successfully.')

        next_param = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not url.is_safe_url(next_param):
            return flask.abort(400)

        return flask.redirect(next_param or flask.url_for('index'))

    context["form"] = form
    return flask.render_template('login.html', **context)


@_app.route("/launch", methods=['POST'])
def launch():
    if flask.request.method == 'POST':
        if flask.request.form['command'] != '':
            tasks.put(Task(flask.request.form['command']))

    return flask.redirect('/')


@_app.route('/details', methods=['GET'])
def details():
    return "Task #%04d<br/>Not implemented yet!" % int(flask.request.args["task_id"])


@_app.route('/_table')
def task_table():
    return flask.render_template("task_table.html", full_task_list=full_task_list)
