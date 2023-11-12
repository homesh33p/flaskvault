import os 

# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration class. Contains 
    default configuration settings + configuration 
    settings applicable to all environments.
    """
    # Default settings
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY')
    HOST = os.getenv("HOST")
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")    
    
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    APP_ID = os.getenv("APP_ID")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL ')
    # RESULT_BACKEND = os.getenv('RESULT_BACKEND')

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True     
    DATABASE = os.environ.get('DATABASE') or 'dev'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
							  f"postgresql+psycopg2://{Config.USER}:{Config.PASSWORD}" \
							  f"@{Config.HOST}/{DATABASE}"

class TestingConfig(Config):
    FLASK_ENV = 'testing'
    TESTING = True
    WTF_CSRF_ENABLED = False    
    DATABASE = os.environ.get('DATABASE') or 'test'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
							  f"postgresql+psycopg2://{Config.USER}:{Config.PASSWORD}" \
							  f"@{Config.HOST}/{DATABASE}"

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DATABASE = os.environ.get('DATABASE') or 'prod'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
							  f"postgresql+psycopg2://{Config.USER}:{Config.PASSWORD}" \
							  f"@{Config.HOST}/{DATABASE}"

config_dict = dict(
    production = ProductionConfig,
    development = DevelopmentConfig,
    testing = TestingConfig
)