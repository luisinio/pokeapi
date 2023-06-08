""" This module contains the routes of the app """
from flask import jsonify, render_template
from app import app
from app.controllers import get_berries_statics, generate_histogram


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


@app.route("/allBerryStats/histogram", methods=["GET"])
def get_histogram():
    """create a histogram from the data of the berries"""
    response_headers = {"Content-Type": "text/html"}
    histogram_html = generate_histogram()
    return (
        render_template(
            "berries_histogram.html",
            histogram_html=histogram_html,
        ),
        200,
        response_headers,
    )
