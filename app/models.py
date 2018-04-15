from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    commands = db.relationship('Command', backref='issuer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class CommandType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(64), index=True, unique=True)
    script_name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<CommandType {}>'.format(self.keyword)


class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    command = db.Column(db.ForeignKey('command_type.id'))
    user = db.Column(db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Command [{0} ran {1}>'.format(self.user, self.command)
