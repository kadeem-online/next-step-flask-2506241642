# standard library imports
import os


class AppConfiguration:
    DEBUG = False
    SECRET_KEY = "secret_key"
    TESTING = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfiguration(AppConfiguration):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///app_development.db"
    )


class TestingConfiguration(AppConfiguration):
    TESTING = True


class ProductionConfiguration(AppConfiguration):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "production_secret_key")
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///app_production.db"
    )
