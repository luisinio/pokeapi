""" This module contains the routes of the app """
from flask import jsonify
from app import app
from app.controllers import get_berries_statics


# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(error):  # pylint: disable=unused-argument
    """404 error handler"""
    return (
        jsonify(
            {
                "error": "Page not found",
                "message": "The requested page does not exist.",
            }
        ),
        404,
    )


@app.route("/allBerryStats", methods=["GET"])
def get_data():
    """get all the data from the url and add it to the data_berries dict"""
    response_headers = {"Content-Type": "application/json"}
    data = get_berries_statics()
    return data, 200, response_headers
