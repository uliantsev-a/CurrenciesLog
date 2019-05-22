# project/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    DEBUG = False
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Database variables
    DB_NAME = os.environ.get('DATABASE_NAME', '')
    DB_USER = os.environ.get('DATABASE_USER', '')
    DB_PASS = os.environ.get('DATABASE_PASSWORD', '')
    DB_HOST = os.environ.get('DATABASE_HOST', 'localhost')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

    LOGFILE_LOADER = 'logs/Loader.log'


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True
    LOGFILE = 'logs/Development.log'


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://test_user:test_pass@localhost/test'


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    DEBUG_TB_ENABLED = False
    LOGFILE = 'logs/Production.log'
