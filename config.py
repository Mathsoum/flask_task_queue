import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Global Flask config
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some_high_tek_generated_key'

    # Log directory to store command outputs
    COMMAND_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(os.path.normcase(__file__))), 'output')

    # SQL Alchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

