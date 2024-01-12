from auth.user_repo import UserRepo
import base64
from flask import Blueprint, request, jsonify, make_response
from auth.schemas import (
    UserBaseSchema,
    UserSchema,
    UserNameSchema,
    UserUpdateSchema,
    UserDeleteSchema,
)
from pydantic import ValidationError
from exceptions import APIError
from .utils import encrypt_string, compare_password, generate_jwt, login_required
from settings import SECRET_KEY

auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/auth", methods=["POST"])
def user_auth():
    auth_header = request.headers.get("Authorization")  # 'Basic SGVtOkhlbSE='
    encoded_credential = auth_header.split(" ")[1]
    decoded_credential = base64.b64decode(encoded_credential).decode(
        "utf-8"
    )  # Hem:Hem!
    username, password = decoded_credential.split(":")
    user_repo = UserRepo()
    user = user_repo.read_by_username(username=username)
    if not user:
        return make_response(jsonify({"message": "No user"}), 204)
    result = compare_password(user_password=password, db_password=user.password)
    if not result:
        return make_response(jsonify({"message": "Incorrect password"}), 401)
    access_token = generate_jwt(
        username=user.username, secret_key=SECRET_KEY
    )  # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiSGVtIiwiaWF0IjoxNzA0OTQ1NjY1LCJleHAiOjE3MDUwMzIwNjV9.BiNv--5VPDg5M9o3LpKg3tE8xq_aCFYztCvOxXlGb4A"  for Hem
    response = make_response(
        jsonify(
            {"message": "Successfully authenticated!", "access_token": access_token}
        ),
        200,
    )
    return response


# Browser hits the endpoint
# Request comes -> Middleware (if any)
# Validation/Deserialization ->Authentication-> Business logic -> database ->
# Validation/Serialization -> Middleware(if any) ->Response
@auth_blueprint.route("/register", methods=["POST"])
def create_user():  # decorated function
    try:
        data = request.json  # deserialize>>> database>>> serialize(dump)>>> response
        # validation and deserialization/ unpackaging from data dictionary and assign to instance
        # deserialization is the process of converting data in a serialized format such as JSON/XML
        # back into its native structure or data strucutre
        user_create_schema = UserBaseSchema(**data)
        username = user_create_schema.username
        password = user_create_schema.password
        encrypted_string = encrypt_string(string=password)
        user_repo = UserRepo()
        # create a new user object in the db
        user = user_repo.create(username=username, password=encrypted_string)
        # create an instance of UserSchema for the purpose of serializing/dumping the user data before sending it as a JSON response
        user_schema = UserSchema(
            id=user.id, username=user.username, password=user.password
        )
        # 'serialized user_schema' can now be included in the JSON response
        # create a JSON response with the user info and HTTP  status code 201 CREATED
        # model_dump() will recursively convert the user_schema instance into a dictionary
        # https://docs.pydantic.dev/latest/concepts/serialization/#modelmodel_dump
        response = make_response(jsonify(user_schema.model_dump()), 201)
        return response
    except ValidationError as exc:
        raise APIError(message=str(exc), status_code=400)


@auth_blueprint.route("/user-read/<username>", methods=["GET"])
@login_required  # decorator function
def read_user(username):
    try:
        userNameSchema = UserNameSchema(username=username)
        user_repo = UserRepo()
        user = user_repo.read_by_username(username=userNameSchema.username)
        user_schema = UserSchema(
            id=user.id, username=user.username, password=user.password
        )
        # will recursively convert the user_schema instance into a dictionary
        response = make_response(jsonify(user_schema.model_dump()), 200)
        return response
    except Exception as exc:
        raise APIError(message=str(exc), status_code=400)


@auth_blueprint.route("/users", methods=["GET"])
@login_required  # decorator function
def read_all_users():
    try:
        user_repo = UserRepo()
        users = user_repo.read_all()
        user_schemas = [
            UserSchema(id=user.id, username=user.username, password=user.password)
            for user in users
        ]
        response = make_response(
            jsonify([user_schema.model_dump() for user_schema in user_schemas]), 200
        )
        return response
    except Exception as exc:
        raise APIError(message=str(exc), status_code=400)


@auth_blueprint.route("/user-update", methods=["PUT"])
@login_required  # decorator function
def update_user():
    try:
        data = request.json
        user_update_schema = UserUpdateSchema(**data)
        username = user_update_schema.username
        password = user_update_schema.password
        encrypted_string = encrypt_string(string=password)
        user_repo = UserRepo()
        updated_user = user_repo.update_by_username(
            username=username, password=encrypted_string
        )
        user_schema = UserSchema(
            id=updated_user.id,
            username=updated_user.username,
            password=updated_user.password,
        )
        response = make_response(jsonify(user_schema.model_dump()), 200)
        return response
    except ValidationError as exc:
        raise APIError(message=str(exc), status_code=400)


@auth_blueprint.route("/user-delete/<username>", methods=["DELETE"])
@login_required  # decorator function
def delete_user(username: str):
    try:
        # user_delete_schema = UserDeleteSchema(username=username)
        user_repo = UserRepo()
        user_repo.delete_by_username(username=username)
        response = make_response(jsonify({"message": "User deleted"}), 204)
        return response
    except ValidationError as exc:
        raise APIError(message=str(exc.json()), status_code=400)
