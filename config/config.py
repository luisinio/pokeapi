"""All settings from the enviroment."""
# pylint: disable= too-few-public-methods
import os


# Settings for Flask
class Config:
    """Set Flask configuration vars."""

    DEBUG = True
    SECRET_KEY = "mysecretkey"
    JSON_SORT_KEYS = False
    template_folder = "app/templates"


# Settings for Flask in development
class DevelopmentConfig(Config):
    """Set Flask configuration vars for development."""

    ENV = "development"


# settings for Flask in production
class ProductionConfig(Config):
    """Set Flask configuration vars for production."""

    ENV = "production"


def get_config():
    """Get the appropriate configuration based on the environment."""
    if os.getenv("FLASK_ENV") == "production":
        return ProductionConfig()
    return DevelopmentConfig()


# Configuration object for Flask
config = get_config()

# Define the url from external microservices
os.environ["URL_BERRY"] = "https://pokeapi.co/api/v2/berry/"
