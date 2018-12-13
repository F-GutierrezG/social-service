import os


class BaseConfig:
    """ Base configuration """
    TESTING = False
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    USERS_SERVICE_MOCK = False
    AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL')
    USERS_SERVICE_URL = os.environ.get('USERS_SERVICE_URL')
    FACEBOOK_OAUTH_URL = os.environ.get('FACEBOOK_OAUTH_URL')
    FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID')
    FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET')
    FACEBOOK_REDIRECT_URI = os.environ.get('FACEBOOK_REDIRECT_URI')
    FACEBOOK_ACCESS_TOKEN_URL = os.environ.get('FACEBOOK_ACCESS_TOKEN_URL')
    AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')


class DevelopmentConfig(BaseConfig):
    """ Development configuration """
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_ECHO = True
    USERS_SERVICE_MOCK = False


class TestingConfig(BaseConfig):
    """ Testing configuration """
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    SQLALCHEMY_ECHO = False
    USERS_SERVICE_MOCK = True


class StagingConfig(BaseConfig):
    """ Staging configuration """
    USERS_SERVICE_MOCK = False


class ProductionConfig(BaseConfig):
    """ Production configuration """
    DEBUG = False
    USERS_SERVICE_MOCK = False
