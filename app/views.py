import flask
from flask_login import login_user, current_user, logout_user

from app import app as _app, tasks, full_task_list
from app.form import TaskForm, LoginForm
from app.runner import Task
from app.models import User

import url
from config import Config


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

    # If user already logged in, redirect to index
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flask.flash('Invalid username or password', 'danger')
            return flask.redirect(flask.url_for('login'))

        login_user(user)
        flask.flash('Logged in successfully.', 'success')

        next_param = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not url.is_safe_url(next_param):
            return flask.abort(400)

        return flask.redirect(next_param or flask.url_for('index'))

    context["form"] = form
    return flask.render_template('login.html', **context)


@_app.route('/logout')
def logout():
    logout_user()
    return flask.redirect(flask.url_for('index'))


@_app.route("/launch", methods=['POST'])
def launch():
    if flask.request.method == 'POST':
        if flask.request.form['command'] != '':
            tasks.put(Task(flask.request.form['command']))

    return flask.redirect('/')


@_app.route('/details/<int:task_id>', methods=['GET'])
def details(task_id):
    try:
        context = base_template_context()
        context["task"] = next(t for t in full_task_list if t.id == int(task_id))
        return flask.render_template("details.html", **context)
    except StopIteration:
        return "Task #%04d<br/>Task not found. Unable to show the details" % int(task_id)


@_app.route('/_table')
def task_table():
    return flask.render_template("task_table.html", full_task_list=full_task_list)


@_app.route('/static/output/<path:path>')
def static_output(path):
    return flask.send_from_directory(Config.COMMAND_OUTPUT_DIR, path)
