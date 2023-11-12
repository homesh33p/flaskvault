import os
import config
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from celery import Celery, Task

import os

import pathlib
from .logSetup import configure_logging

login_manager = LoginManager()

db = SQLAlchemy()
bootstrap = Bootstrap()
migrate = Migrate()

### Application Factory ###
def create_app(test_config=None):

    app = Flask(__name__)

    # Choose the appropriate configuration class based on the environment
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(config.config_dict[os.getenv("FLASK_ENV")])
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    register_extensions(app)

    # Register blueprints
    register_blueprints(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    @app.cli.command("pytestrun")
    def pytestrun():
        """Run the unit tests."""
        import pytest
        pytest.main(['--rootdir', 'tests'])    

    return app

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name,task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])

    celery_app.set_default()
    app.extensions["celery"] = celery_app

def register_celery(app) -> Flask:
    import logging
    app.config.from_mapping(
        CELERY=dict(
            broker_url=os.environ['BROKER_URL'],
            result_backend=os.environ['RESULT_BACKEND'],
            task_ignore_result=os.environ.get('TASK_IGNORE_RESULT',default=True),
            log_path = pathlib.PurePosixPath(os.environ['LOG_PATH']),
            log_level = os.environ.get('WORKER_LOG_LEVEL',default = logging.INFO),
            file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')
            # log_format = '%(asctime)s [%(levelname)s] [%(task_id)s:%(task_name)s] %(message)s'
        ),
    )
    celery_init_app(app)

def register_extensions(app):
    bootstrap.init_app(app)
    from app.models import User
    db.init_app(app)
    migrate.init_app(app=app,db=db)
    login_manager.init_app(app)
    register_celery(app)
    login_manager.login_view = 'auth.login'

### Helper Functions ###
def register_blueprints(app):
    from app.auth import auth_bp
    from app.main import main_bp
    from app.status import status_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(status_bp,url_prefix='/status')

def register_error_handlers(app):

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500
    