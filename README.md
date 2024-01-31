# Authentication Server

Auth is a Flask project that provides JWT token to the registered users so that they can
do CRUD operations in the web services

This project is build on Flask and MongoDB (MongoDB Atlas). Also docker is used for containerization, mainly docker-compose.yml is used for that.

This Auth server generated JWT token which is used by other application such as
Information Server [Information Server](https://github.com/rajan10/information-server)

## Table of Contents

- [Installation](#Installation)
- [Usage](#Usage)
- [Contributing](#Contributing)
- [Guidelines](#Guidelines)
- [Related-Project](#Related-Project)
- [License](#License)
- [Questions](#Questions)

## Installation
In the virtual env terminal, type below command in the terminal to install all dependecies

```
pip install -r requirements.txt
```

## Usage
Install dependencies and run the application or use docke containerization and build the environment and run the application
```
docker-compose up --build
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate

## Guidelines 
Main file is app.py
MongoDb and its configuration connected to this applicaiton
auth_blueprint is used as template
Global error handling/ middleware error handling

Model.py -> User

User is checked with MongoDB and access token is created for UserRepo CRUD operations

UserRepo
Schema for serializaition is used

jwt access token is created once user is verified from db

## Related Project
- [Information-server](https://github.com/rajan10/information-server)

## License
This project is not licensed under the 
[MIT](https://choosealicense.com/licenses/mit/)

## Questions