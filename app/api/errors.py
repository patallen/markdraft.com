from marklib.request import MakeResponse
from api import app


@app.errorhandler(500)
def internal_error(e):
    xhr = MakeResponse(500, error="Internal Server Error")
    return xhr.response


@app.errorhandler(404)
def method_not_allowed(e):
    xhr = MakeResponse(405, error="Method Not Allowed")
    return xhr.response


@app.errorhandler(404)
def not_found(e):
    xhr = MakeResponse(404, error="Not Found")
    return xhr.response


@app.errorhandler(401)
def unauthorized(e):
    xhr = MakeResponse(401, error="Unauthorized")
    return xhr.response


@app.errorhandler(400)
def invalid_request(e):
    xhr = MakeResponse(400, error="Invalid Request")
    return xhr.response
