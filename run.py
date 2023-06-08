""" This file is used to run the application. """
from app import app
from config import config

if __name__ == "__main__":
    app.config.from_object(config.DevelopmentConfig)
    app.run(debug=True)
