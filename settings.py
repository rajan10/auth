from decouple import config

SECRET_KEY = config("SECRET_KEY")
DB_NAME = config("DB_NAME")
DB_HOST = config("DB_HOST")
