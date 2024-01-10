from mongoengine import Document, StringField


# define a MongoDB document schema. 'mongoengine' is an ODM(Object Document Mapper) library for MongoDB in Python
class User(Document):
    username = StringField(max_length=400, required=True)
    password = StringField(max_length=400, required=True)
