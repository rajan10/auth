# Authentication Server

This is authentication server build on Flask f/w

Main file is app.py
MongoDb and its configuration connected to this applicaiton
auth_blueprint is used as template
Global error handling/ middleware error handling

Model.py -> User

User is checked with MongoDB and access token is created for UserRepo CRUD operations

UserRepo

Schema for serializaition is used

jwt access token is created once user is verified from db
