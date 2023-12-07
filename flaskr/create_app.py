import os

from flask import Flask
import logging

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello World!'

    from . import db
    db.init_app(app)

    from flaskr.routes.auth import auth
    app.register_blueprint(auth.bp)

    from flaskr.routes.blog import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/',endpoint='index')

    return app

def init_log():
    from flask.logging import default_handler
    from .common.log.log_formatter import request_formatter
    from .common.log.logger import RunLogger
    log_service = RunLogger(level=logging.DEBUG,
                            formatter=request_formatter,
                            filename="flaskr.log")
    file_handle = log_service.get_file_handle()
    stream_handle = log_service.get_stream_handle()
    logger = log_service.logger
    logger.addHandler(file_handle)
    logger.addHandler(stream_handle)
    return logger