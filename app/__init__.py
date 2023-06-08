""" File that initializes the application """
from flask import Flask

app = Flask(__name__)

# App configuration
app.config.from_object("config.config")

# Import routes and models
from app import routes, models  # pylint: disable=wrong-import-position
