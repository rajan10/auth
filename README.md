# Authentication Server

This is authentication server build on Flask f/w

This project is build on Flask and MongoDB

This Auth server generated JWT token which is used by other application such as
Information Server [link](https://github.com/rajan10/information-server)

Main file is app.py
MongoDb and its configuration connected to this applicaiton
auth_blueprint is used as template
Global error handling/ middleware error handling

Model.py -> User

User is checked with MongoDB and access token is created for UserRepo CRUD operations

UserRepo

Schema for serializaition is used

jwt access token is created once user is verified from db
