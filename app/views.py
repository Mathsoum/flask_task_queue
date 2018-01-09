import flask
from flask_login import login_user

from app import app, tasks, full_task_list
from app.form import TaskForm, LoginForm
from app.runner import Task
from app.user import User

import url


@app.route('/')
def hello_world():
    return flask.render_template("main.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    return flask.render_template('login.html', form=form)


@app.route('/add', methods=['POST', 'GET'])
def add_task():
    if flask.request.method == 'POST':
        if flask.request.form['message'] != '':
            tasks.put(Task(flask.request.form['message']))

    form = TaskForm()
    return flask.render_template("addition.html", form=form, full_task_list=full_task_list)


@app.route('/_table')
def task_table():
    return flask.render_template("task_table.html", full_task_list=full_task_list)


@app.route('/_add_numbers')
def add_numbers():
    a = flask.request.args.get('a', 0, type=int)
    b = flask.request.args.get('b', 0, type=int)
    return flask.jsonify(result=a + b)
