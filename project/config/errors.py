from flask import jsonify, make_response
from werkzeug.exceptions import HTTPException
import json as json

from marshmallow import ValidationError

errors = {
    "EmailNotFoundException": {"message": "hello", "status": 404},
    "ValidationError": {"message": "hi", "status": 422},
}


def register_error_handlers(app: object) -> None:
    app.register_error_handler(422, handle_422)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(429, handle_429)
    # app.register_error_handler(EmailNotFoundException, handle_HTTPException)
    # app.register_error_handler(HTTPException, handle_HTTPException)


def handle_422(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return make_response(jsonify({"errors": messages}), err.code, headers)
    else:
        return make_response(jsonify({"errors": messages}), err.code)


def handle_404(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Not found."])
    if headers:
        return make_response(jsonify({"errors": messages}), err.code, headers)
    else:
        return make_response(jsonify({"errors": messages}), err.code)


def handle_429(err):
    description = err.description
    return make_response(
        jsonify({"errors": "ratelimit exceeded %s" % description}), err.code
    )


def handle_HTTPException(err):
    # headers = err.data.get("headers", None)
    # messages = err.data.get("messages", ["Not found."])
    # if headers:
    #     return jsonify({"errors": messages}), err.code, headers
    # else:
    #     return jsonify({"errors": messages}), err.code
    response = err.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": err.code,
            "name": err.name,
            "description": err.description,
        }
    )
    response.content_type = "application/json"
    return response
