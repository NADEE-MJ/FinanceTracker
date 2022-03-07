from flask import jsonify


def register_error_handlers(app: object) -> None:
    app.register_error_handler(422, handle_422_Test)


def handle_422_Test(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code
