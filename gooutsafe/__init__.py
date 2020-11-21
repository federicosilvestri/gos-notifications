"""
Flask initialization
"""
import os

__version__ = '0.1'

from celery import Celery
import connexion
from flask_environments import Environments
from flask import Flask
from flask_mongoengine import MongoEngine
import logging

db: MongoEngine
app: Flask
api_app: connexion.FlaskApp
logger: logging.Logger
celery: Celery


def create_app():
    """
    This method create the Flask application.
    :return: Flask App Object
    """
    global db
    global app
    global api_app
    global celery

    # first initialize the logger
    init_logger()

    api_app = connexion.FlaskApp(
        __name__,
        server='flask'
    )

    # getting the flask app
    app = api_app.app

    flask_env = os.getenv('FLASK_ENV', 'None')
    if flask_env == 'development':
        config_object = 'config.DevConfig'
    elif flask_env == 'testing':
        config_object = 'config.TestConfig'
    elif flask_env == 'production':
        config_object = 'config.ProdConfig'
    else:
        raise RuntimeError(
            "%s is not recognized as valid app environment. You have to setup the environment!" % flask_env)

    # Load config
    env = Environments(app)
    env.from_object(config_object)

    # creating celery
    celery = make_celery(app)

    # loading communications
    import gooutsafe.comm as comm

    if flask_env != 'testing':
        comm.init_rabbit_mq()
    else:
        comm.disabled = True

    if flask_env != 'production':
        # disable communication for testing purposes
        comm.disabled = True
    else:
        comm.init_rabbit_mq()

    # checking the environment
    if flask_env != 'testing':
        db = MongoEngine(
            app=app
        )
    else:
        # Loading the MongoMock
        db = None

    # requiring the list of models
    import gooutsafe.models

    # registering to api app all specifications
    register_specifications(api_app)

    return app


def init_logger():
    global logger
    """
    Initialize the internal application logger.
    :return: None
    """
    logger = logging.getLogger(__name__)
    from flask.logging import default_handler
    logger.addHandler(default_handler)


def register_specifications(_api_app):
    """
    This function registers all resources in the flask application
    :param _api_app: Flask Application Object
    :return: None
    """

    # we need to scan the specifications package and add all yaml files.
    from importlib_resources import files
    folder = files('gooutsafe.specifications')
    for _, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = folder.joinpath(file)
                _api_app.add_api(file_path)


def make_celery(_app):
    """
    This function create celery instance.

    :param _app: Application Object
    :return: Celery instance
    """
    broker_uri = 'pyamqp://%s:%s/%s' % (
        os.getenv('RABBIT_MQ_HOST', None),
        os.getenv('RABBIT_MQ_PORT', None),
        os.getenv('RABBIT_MQ_VHOST', None)
    )
    backend_uri = 'mongodb://%s:%s/%s' % (
        os.getenv('MONGODB_HOST', None),
        os.getenv('MONGODB_PORT', None),
        os.getenv('MONGODB_DB', None)
    )
    """
    @TODO: add a control to variables.
    """

    _celery = Celery(
        _app.name,
        broker=broker_uri,
        backend=backend_uri
    )
    _celery.conf.timezone = 'Europe/Rome'
    _celery.conf.update(_app.config)

    """
    Importing the tasks with celery
    """
    import gooutsafe.tasks

    class ContextTask(_celery.Task):
        def __call__(self, *args, **kwargs):
            with _app.app_context():
                return self.run(*args, **kwargs)

    return _celery


def create_app_with_celery():
    return create_app(), celery
