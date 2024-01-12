from flask import Flask, jsonify, make_response
from auth.urls import auth_blueprint
from database import db
from exceptions import APIError

from .settings import DB_NAME, DB_HOST

app = Flask(__name__)
app.register_blueprint(auth_blueprint)

app.config["MONGODB_SETTINGS"] = [{"db": DB_NAME, "host": DB_HOST}]
db.init_app(app)


@app.errorhandler(Exception)
def handle_exception(exc):
    if not isinstance(exc, APIError):
        if hasattr(exc, "code"):
            status_code = exc.code
        else:
            status_code = 500
        exc = APIError(
            message=str(exc), status_code=status_code
        )  # if not APIError (it means some other type of exception that was not explicityly handled)
        # in such case, the code create a new instance of APIError with default values, set status code to 500
    response = jsonify({"message": exc.message})
    response.status_code = exc.status_code
    return response


@app.route("/")
def health_status():
    response = make_response(jsonify({"message": "Server is running"}), 200)
    return response
