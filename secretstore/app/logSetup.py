import pathlib
import os
from celery.app.log import Logging
from celery.utils.log import get_logger 

def configure_celery_logging(app):

    celery_app = app.extensions["celery"]
    
    cellogspath = celery_app.conf.log_path / "celery.log"
    # workerlogpath = celery_app.conf.log_path / "worker.log"

    # Create a file formatter object
    # file_formatter = celery_app.conf.file_formatter
    level = celery_app.conf.log_level

    loggingModule = Logging(celery_app)
    loggingModule.setup(loglevel=level,logfile=cellogspath)

def configure_logging(app):

    import logging
    from flask.logging import default_handler
    from logging.handlers import RotatingFileHandler

    # Deactivate the default flask logger so that log messages don't get duplicated 
    app.logger.removeHandler(default_handler)

    # logspath = pathlib.Path(app.root_path).parent/ os.environ['LOG_PATH']/ 'access.log'
    logspath = pathlib.PurePosixPath(os.environ['LOG_PATH'])/ 'access.log'

    # Create a file handler object
    file_handler = RotatingFileHandler(logspath, maxBytes=16384, backupCount=3)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(os.environ.get('APP_LOG_LEVEL',default='INFO'))

    # Create a file formatter object
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)

    configure_celery_logging(app) 
       