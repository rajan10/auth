import bcrypt
from datetime import datetime, timedelta
import jwt
from functools import wraps
from flask import request, jsonify, make_response
from jwt import InvalidTokenError, ExpiredSignatureError


def encrypt_string(string: str) -> str:
    bytes = string.encode("utf-8")  # b'abc123'
    salt = bcrypt.gensalt()  # b'$2b$12$eGyZOEYfTfHIbXIoRkSyLO'
    # hashing the password with the salt
    encrypted_bytes = bcrypt.hashpw(bytes, salt)  # b'$2b$12$9b/2.w32r4c9.98h71.2.12
    encrypted_string = encrypted_bytes.decode(
        "utf-8"
    )  # '$2b$12$eGyZOEYfTfHIbXIoRkSyLOY7jcm04.XZpuM.oPQl9s5FeL65f7Dfa'
    return encrypted_string


# encrypt = encrypt_string(
#     "abc123"
# )  # '$2b$12$eGyZOEYfTfHIbXIoRkSyLOY7jcm04.XZpuM.oPQl9s5FeL65f7Dfa'


# # encrypted password is already in db, so we need to get it from db
# db_password = {"password": encrypt}
# db_password = db_password.get("password")
# db_password_bytes = db_password.encode("utf-8")  # $2b$12$9b/2.w32r4c9.98h71.2.12
# print(db_password_bytes)  # $2b$12$9b/2.w32r4c9.98h71.2.12


def compare_password(user_password: str, db_password: str) -> bool:
    user_password_bytes = user_password.encode("utf-8")  # b'Hem!'

    result = bcrypt.checkpw(user_password_bytes, db_password.encode("utf-8"))
    return result


# print(compare_password("abc123", db_password_bytes))  # True


def generate_jwt(username, secret_key):
    issued_at = datetime.utcnow()
    expiration_time = issued_at + timedelta(days=1)
    payload = {
        "user": f"{username}",
        "iat": issued_at,
        "exp": expiration_time,
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


def login_required(func: callable):
    @wraps(
        func
    )  # is a decorator function that updates the wrapper function to look like the decorated function(func).This is often used
    # to preserve metadata such as the the function name and docstring
    def wrapper(
        *args, **kwargs
    ):  # this is the actual decorated function that will  replace the original function when
        # 'authorization_required' is appled eg hello_world or def login()
        try:  # token extraction and validation
            authorization_header = request.headers.get("Authorization")
            if not authorization_header or not authorization_header.startswith(
                "Bearer "
            ):
                return make_response(
                    jsonify({"message": "Missing Authorization Header"}), 400
                )

            access_token = request.headers["Authorization"].split(" ")[
                1
            ]  # Basic Sm9objpKb2huIQ==
            decoded_payload = jwt.decode(access_token, "test", algorithms=["HS256"])
            if not decoded_payload:
                return make_response(
                    jsonify({"message": "Incorrect access token"}), 400
                )
            return func(
                *args, **kwargs
            )  # if access token is valid, the original 'func' is called with its arguments and keyword arguments
        except (InvalidTokenError, ExpiredSignatureError) as exc:
            return make_response(
                jsonify({"message": f"Invalid token signature {str(exc)}"}), 400
            )
        except Exception as exc:
            return make_response(jsonify({"message": str(exc)}), 500)

    return wrapper
